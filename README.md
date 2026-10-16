# Hotel Morgenrot

Einfache deutsche Hotel-Webseite mit lokaler Gästeverwaltung und SQLite-Datenbank. Benötigt Python 3.12 oder neuer, keine zusätzlichen Pakete.

## Starten

```sh
cd /workspace/Chatgpt-codex-tests
python3 app.py
```

Im Browser unter `http://127.0.0.1:8000` öffnen. Mit Strg+C beenden.

Gäste lassen sich mit Name, E-Mail, Zimmerkategorie und Aufenthaltsdaten erfassen und löschen. Die Daten bleiben in `data/hotel.db` gespeichert; diese Datei wird nicht in Git aufgenommen. Für eine Sicherung den Server stoppen und die Datenbankdatei kopieren.

Die Zimmer und Preise sind Beispiele. Es gibt keine Verfügbarkeitsprüfung oder Onlinebuchung.

Die Anwendung ist ein lokaler Prototyp ohne Anmeldung. Vor öffentlichem Betrieb mit echten Gästedaten sind insbesondere eine geschützte Mitarbeiterverwaltung, HTTPS und ein Datenschutzkonzept erforderlich. Der Server lauscht deshalb ausschließlich auf der lokalen Schnittstelle.
