# FIMATO App - Softwarearchitektur

## Übersicht
Die FIMATO App ist eine Webanwendung, die auf einer Client-Server-Architektur basiert.

## Technologie-Stack
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Datenbank**: SQLite (erweiterbar auf andere Datenbanken)

## Architekturkomponenten

### Backend (Server)
- Flask-Framework für RESTful API
- Modulare Struktur mit Blueprints
- Model-View-Controller (MVC) Pattern
- Authentifizierung und Autorisierung
- Datenbankanbindung

### Frontend (Client)
- Responsive HTML Templates
- Modernes CSS-Layout
- JavaScript für interaktive Funktionen
- AJAX für asynchrone Serveranfragen

## Verzeichnisstruktur
```
fimato_app/                          # 🔷 Projekt-Root
│
├── venv/                            # 🟢 Virtuelle Umgebung
│
├── app/                             # 🔵 Flask-Anwendung
│   ├── __init__.py                  # App Factory + Blueprint-Registrierung
│   │
│   ├── main/                        # Hauptbereich der App
│   │   ├── __init__.py              
│   │   ├── routes.py                
│   │   └── templates/
│   │
│   ├── auth/                        # Authentifizierung
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │
│   ├── models/                      # Datenbankmodelle
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── static/                      # Frontend Assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── templates/                   # Gemeinsame Templates
│
├── config.py                        # Konfigurationen
├── run.py                           # Startpunkt
├── requirements.txt                 # Abhängigkeiten
└── README.md                        # Projektdokumentation
```

## Datenfluss
1. Client sendet Anfrage an Server
2. Server verarbeitet Anfrage über entsprechende Route
3. Controller/Route führt Geschäftslogik aus
4. Datenbankanfragen werden über Models abgewickelt
5. Server rendert Template oder sendet JSON-Response
6. Client zeigt Ergebnis an

## Sicherheitsaspekte
- Sichere Passwortspeicherung
- CSRF-Schutz
- Session-Management
- Input-Validierung
- XSS-Prävention 