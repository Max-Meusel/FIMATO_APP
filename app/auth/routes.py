from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from app.auth import bp
from app.models.user import User
from app import db
from datetime import datetime

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
        
        # Validierung der Eingaben
        if not all([firstname, lastname, birthday_str, email, password, password2]):
            flash('Bitte füllen Sie alle Felder aus.', 'error')
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
            email=email
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registrierung erfolgreich! Sie können sich jetzt einloggen.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', title='Register')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index')) 