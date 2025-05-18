from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    # Überprüfe existierende Benutzer
    users = User.query.all()
    print("\nExistierende Benutzer:")
    for user in users:
        print(f"Username: {user.username}, Email: {user.email}")
    
    # Erstelle einen Testbenutzer
    if not User.query.filter_by(username="testuser").first():
        test_user = User(username="testuser", email="test@example.com")
        test_user.set_password("test123")
        db.session.add(test_user)
        db.session.commit()
        print("\nTestbenutzer wurde erstellt!")
    else:
        print("\nTestbenutzer existiert bereits!") 