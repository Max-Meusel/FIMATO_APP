from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from app.user_ui import bp
from app import db
from app.models.user import User

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user_ui/dashboard.html', title='Dashboard')

@bp.route('/navigation')
@login_required
def navigation():
    return render_template('user_ui/navigation.html', title='Navigation')

@bp.route('/profile')
@login_required
def profile():
    return render_template('user_ui/settings/profile.html', title='Profil')

# Haushaltsbuch
@bp.route('/transactions')
@login_required
def transactions():
    return render_template('user_ui/household_book/transactions.html', title='Transaktionen')

@bp.route('/standing-orders')
@login_required
def standing_orders():
    return render_template('user_ui/household_book/standing_orders.html', title='Daueraufträge')

@bp.route('/contracts')
@login_required
def contracts():
    return render_template('user_ui/household_book/contracts.html', title='Verträge & Abos')

# Vermögensverwaltung
@bp.route('/securities')
@login_required
def securities():
    return render_template('user_ui/asset_management/securities.html', title='Wertpapierdepot')

@bp.route('/real-estate')
@login_required
def real_estate():
    return render_template('user_ui/asset_management/real_estate.html', title='Immobilien')

@bp.route('/vehicles')
@login_required
def vehicles():
    return render_template('user_ui/asset_management/vehicles.html', title='Fahrzeuge')

@bp.route('/inventory')
@login_required
def inventory():
    return render_template('user_ui/asset_management/inventory.html', title='Inventarliste')

@bp.route('/other-assets')
@login_required
def other_assets():
    return render_template('user_ui/asset_management/other_assets.html', title='Sonstige Vermögenswerte')

# Finanzreport
@bp.route('/income')
@login_required
def income():
    return render_template('user_ui/financial_report/income.html', title='Einnahmen')

@bp.route('/expenses')
@login_required
def expenses():
    return render_template('user_ui/financial_report/expenses.html', title='Ausgaben')

@bp.route('/asset-development')
@login_required
def asset_development():
    return render_template('user_ui/financial_report/asset_development.html', title='Vermögensentwicklung')

# Ziele
@bp.route('/life-planning')
@login_required
def life_planning():
    return render_template('user_ui/goals/life_planning.html', title='Lebensplanung')

@bp.route('/goals-overview')
@login_required
def goals_overview():
    return render_template('user_ui/goals/goals_overview.html', title='Übersicht Ziele')

# Bankkonten
@bp.route('/bank-accounts')
@login_required
def bank_accounts():
    return render_template('user_ui/bank_accounts/accounts.html', title='Bankkonten')

@bp.route('/depots')
@login_required
def depots():
    return render_template('user_ui/bank_accounts/depots.html', title='Depots')

# Einstellungen
@bp.route('/general-settings')
@login_required
def general_settings():
    return render_template('user_ui/settings/general_settings.html', title='Allgemeine Einstellungen')

@bp.route('/categories')
@login_required
def categories():
    return render_template('user_ui/settings/categories.html', title='Kategorien')

@bp.route('/update-email', methods=['POST'])
@login_required
def update_email():
    new_email = request.form.get('new_email')
    password = request.form.get('password')

    if not new_email or not password:
        flash('Bitte füllen Sie alle Felder aus.', 'error')
        return redirect(url_for('user_ui.general_settings'))

    if not current_user.check_password(password):
        flash('Das eingegebene Passwort ist nicht korrekt.', 'error')
        return redirect(url_for('user_ui.general_settings'))

    if current_user.email == new_email:
        flash('Die neue E-Mail-Adresse muss sich von der aktuellen unterscheiden.', 'error')
        return redirect(url_for('user_ui.general_settings'))

    current_user.email = new_email
    db.session.commit()
    flash('Ihre E-Mail-Adresse wurde erfolgreich aktualisiert.', 'success')
    return redirect(url_for('user_ui.general_settings'))

@bp.route('/update-password', methods=['POST'])
@login_required
def update_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not all([current_password, new_password, confirm_password]):
        flash('Bitte füllen Sie alle Felder aus.', 'error')
        return redirect(url_for('user_ui.general_settings'))

    if not current_user.check_password(current_password):
        flash('Das aktuelle Passwort ist nicht korrekt.', 'error')
        return redirect(url_for('user_ui.general_settings'))

    if new_password != confirm_password:
        flash('Die neuen Passwörter stimmen nicht überein.', 'error')
        return redirect(url_for('user_ui.general_settings'))

    current_user.set_password(new_password)
    db.session.commit()
    flash('Ihr Passwort wurde erfolgreich aktualisiert.', 'success')
    return redirect(url_for('user_ui.general_settings'))

@bp.route('/update-newsletter', methods=['POST'])
@login_required
def update_newsletter():
    newsletter = request.form.get('newsletter') == 'on'
    current_user.newsletter_subscription = newsletter
    db.session.commit()
    flash('Ihre Newsletter-Einstellungen wurden aktualisiert.', 'success')
    return redirect(url_for('user_ui.general_settings'))

@bp.route('/delete-account')
@login_required
def delete_account():
    user_id = current_user.id
    logout_user()
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Ihr Account wurde erfolgreich gelöscht.', 'success')
    return redirect(url_for('main.index')) 