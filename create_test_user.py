from app import create_app, db
from app.models.user import User
from datetime import datetime

app = create_app()
with app.app_context():
    # Erstelle Test-Benutzer
    test_user = User(
        firstname='Max',
        lastname='Mustermann',
        birthday=datetime.strptime('01.01.1990', '%d.%m.%Y').date(),
        email='max@test.de'
    )
    test_user.set_password('test123')
    
    # Prüfe ob Benutzer bereits existiert
    existing_user = User.query.filter_by(email='max@test.de').first()
    if not existing_user:
        db.session.add(test_user)
        db.session.commit()
        print('\nTest-Benutzer wurde erstellt!')
        print('E-Mail: max@test.de')
        print('Passwort: test123')
    else:
        print('\nBenutzer mit dieser E-Mail existiert bereits!')
    
    # Zeige alle Benutzer an
    print('\nAlle Benutzer in der Datenbank:')
    users = User.query.all()
    for user in users:
        print(f'Name: {user.firstname} {user.lastname}, E-Mail: {user.email}, Geburtstag: {user.birthday}') 