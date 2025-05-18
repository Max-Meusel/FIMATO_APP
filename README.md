# FIMATO App

Eine moderne Webanwendung basierend auf Flask, HTML, CSS und JavaScript.

## Projektstruktur

Die Anwendung folgt einer modularen Struktur mit klarer Trennung von Frontend und Backend:

- `app/`: Hauptverzeichnis der Flask-Anwendung
  - `main/`: Hauptfunktionalität
  - `auth/`: Authentifizierung
  - `static/`: Frontend-Assets (CSS, JS, Bilder)
  - `templates/`: HTML-Templates

## Installation

1. Python-Umgebung einrichten:
```bash
# Virtuelle Umgebung erstellen
python3 -m venv venv

# Virtuelle Umgebung aktivieren
# Unter Windows:
venv\Scripts\activate
# Unter Unix oder MacOS:
source venv/bin/activate
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Umgebungsvariablen konfigurieren:
```bash
# .env Datei erstellen und anpassen
cp .env.example .env
```

## Entwicklung

1. Entwicklungsserver starten:
```bash
python run.py
```

2. Im Browser öffnen:
```
http://localhost:5000
```

## Features

- Moderne, responsive Benutzeroberfläche
- Benutzerauthentifizierung
- Flash-Nachrichten für Feedback
- Formularvalidierung
- Responsive Design

## Technologie-Stack

- Backend: Python Flask
- Frontend: HTML5, CSS3, JavaScript
- Datenbank: SQLite (erweiterbar)
- Authentifizierung: Flask-Login
- Styling: Custom CSS mit Variablen

## Lizenz

MIT 