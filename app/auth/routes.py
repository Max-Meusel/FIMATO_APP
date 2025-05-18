from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from app.auth import bp
from app.models.user import User
from app.models.security_question import SecurityQuestion
from app import db
from datetime import datetime
from sqlalchemy import text

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember_me') is not None
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('user_dashboard.dashboard'))
        flash('Ungültige E-Mail oder Passwort', 'error')
    
    return render_template('auth/login.html', title='Login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard.dashboard'))
    
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthday_str = request.form.get('birthday')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        # Neue Felder
        question_type = request.form.get('question_type')
        security_question = request.form.get('security_question')
        custom_security_question = request.form.get('custom_security_question')
        security_answer = request.form.get('security_answer')
        accept_terms = request.form.get('accept_terms') == 'on'
        accept_privacy = request.form.get('accept_privacy') == 'on'
        newsletter = request.form.get('newsletter') == 'on'
        
        # Validierung der Eingaben
        if not all([firstname, lastname, birthday_str, email, password, password2, security_answer]):
            flash('Bitte füllen Sie alle Pflichtfelder aus.', 'error')
            return redirect(url_for('auth.register'))
        
        if not accept_terms or not accept_privacy:
            flash('Sie müssen den AGB und der Datenschutzerklärung zustimmen.', 'error')
            return redirect(url_for('auth.register'))
        
        if password != password2:
            flash('Die Passwörter stimmen nicht überein', 'error')
            return redirect(url_for('auth.register'))
        
        # Validierung des Geburtsdatums
        try:
            birthday = datetime.strptime(birthday_str, '%d.%m.%Y').date()
        except ValueError:
            flash('Ungültiges Datumsformat. Bitte verwenden Sie DD.MM.YYYY', 'error')
            return redirect(url_for('auth.register'))
        
        # Überprüfung auf existierende E-Mail
        if User.query.filter_by(email=email).first():
            flash('Diese E-Mail-Adresse wird bereits verwendet', 'error')
            return redirect(url_for('auth.register'))
        
        # Erstelle neuen Benutzer
        user = User(
            firstname=firstname,
            lastname=lastname,
            birthday=birthday,
            email=email,
            accept_terms=accept_terms,
            accept_privacy=accept_privacy,
            newsletter_subscription=newsletter
        )
        print(f"Creating new user with email: {email}")  # Debug-Ausgabe
        user.set_password(password)
        
        # Erstelle Sicherheitsfrage
        security_question_text = security_question if question_type == 'standard' else custom_security_question
        security_question_obj = SecurityQuestion(
            user=user,
            question_type=question_type,
            question_text=security_question_text
        )
        security_question_obj.set_answer(security_answer)
        
        try:
            db.session.add(user)
            db.session.add(security_question_obj)
            db.session.commit()
            print(f"Successfully created user with email: {email}")  # Debug-Ausgabe
            flash('Registrierung erfolgreich! Sie können sich jetzt einloggen.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {str(e)}")  # Debug-Ausgabe
            flash('Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', title='Register')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()  # Normalisiere die E-Mail
        print(f"Searching for email: '{email}'")  # Debug mit Anführungszeichen
        
        # Überprüfen Sie alle Benutzer in der Datenbank
        all_users = User.query.all()
        print("All users in database:")
        for u in all_users:
            print(f"User ID: {u.id}, Email: '{u.email}'")  # Debug mit ID und Anführungszeichen
        
        # Versuche case-insensitive Suche
        user = User.query.filter(User.email.ilike(email)).first()
        
        if user:
            print(f"User found: ID={user.id}, Email='{user.email}'")  # Debug mit mehr Details
            session['reset_user_id'] = user.id
            return redirect(url_for('auth.verify_security_question'))
        else:
            print(f"No user found with email '{email}' (case-insensitive search)")  # Detaillierte Debug-Info
            # Versuche direkte Datenbankabfrage
            result = db.session.execute(text("SELECT id, email FROM user")).fetchall()
            print("Direct database query results:")
            for row in result:
                print(f"ID: {row[0]}, Email: '{row[1]}'")
            
            flash('Diese E-Mail-Adresse wurde nicht gefunden.', 'error')
    
    return render_template('auth/forgot_password.html', title='Passwort vergessen')

@bp.route('/verify-security-question', methods=['GET', 'POST'])
def verify_security_question():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard.dashboard'))
    
    user_id = session.get('reset_user_id')
    if not user_id:
        return redirect(url_for('auth.forgot_password'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        answer = request.form.get('answer')
        if user.security_question.check_answer(answer):
            session['can_reset_password'] = True
            return redirect(url_for('auth.reset_password'))
        else:
            flash('Die Antwort ist nicht korrekt.', 'error')
    
    return render_template('auth/verify_security_question.html',
                         security_question=user.security_question.question_text,
                         title='Sicherheitsfrage')

@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard.dashboard'))
    
    if not session.get('can_reset_password'):
        return redirect(url_for('auth.forgot_password'))
    
    user_id = session.get('reset_user_id')
    if not user_id:
        return redirect(url_for('auth.forgot_password'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        if not password or not password2:
            flash('Bitte füllen Sie alle Felder aus.', 'error')
        elif password != password2:
            flash('Die Passwörter stimmen nicht überein.', 'error')
        else:
            user.set_password(password)
            db.session.commit()
            
            # Lösche die Session-Variablen
            session.pop('reset_user_id', None)
            session.pop('can_reset_password', None)
            
            flash('Ihr Passwort wurde erfolgreich zurückgesetzt. Sie können sich jetzt einloggen.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title='Passwort zurücksetzen') 