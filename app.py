from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import sqlite3
from datetime import date

ROOT = Path(__file__).parent
DB = ROOT / 'data' / 'hotel.db'


def connect():
    DB.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    connection.execute('''CREATE TABLE IF NOT EXISTS guests (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
        room TEXT NOT NULL, arrival TEXT NOT NULL, departure TEXT NOT NULL)''')
    return connection


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, content, kind='application/json; charset=utf-8'):
        body = content.encode() if isinstance(content, str) else json.dumps(content).encode()
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/':
            self.respond(200, (ROOT / 'index.html').read_text(), 'text/html; charset=utf-8')
        elif self.path == '/api/guests':
            with connect() as db:
                guests = [dict(row) for row in db.execute('SELECT * FROM guests ORDER BY arrival, id')]
            self.respond(200, guests)
        else:
            self.respond(404, {'error': 'Nicht gefunden'})

    def do_POST(self):
        if self.path != '/api/guests':
            return self.respond(404, {'error': 'Nicht gefunden'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 8192:
                raise ValueError()
            data = json.loads(self.rfile.read(length))
            fields = ['name', 'email', 'room', 'arrival', 'departure']
            values = [data[key].strip() for key in fields]
            if any(not value or len(value) > 200 for value in values):
                raise ValueError()
            if '@' not in values[1] or values[2] not in ('Einzelzimmer', 'Doppelzimmer', 'Suite'):
                raise ValueError()
            if date.fromisoformat(values[3]) >= date.fromisoformat(values[4]):
                raise ValueError()
        except (ValueError, KeyError, TypeError, AttributeError):
            return self.respond(400, {'error': 'Bitte alle Felder korrekt ausfüllen. Die Abreise muss nach der Anreise liegen.'})
        with connect() as db:
            cursor = db.execute('INSERT INTO guests (name,email,room,arrival,departure) VALUES (?,?,?,?,?)', values)
            guest_id = cursor.lastrowid
        self.respond(201, {'id': guest_id})

    def do_DELETE(self):
        try:
            if not self.path.startswith('/api/guests/'):
                raise ValueError()
            guest_id = int(self.path.removeprefix('/api/guests/'))
        except ValueError:
            return self.respond(404, {'error': 'Nicht gefunden'})
        with connect() as db:
            cursor = db.execute('DELETE FROM guests WHERE id=?', (guest_id,))
        self.respond(200 if cursor.rowcount else 404, {'deleted': bool(cursor.rowcount)})


if __name__ == '__main__':
    with connect():
        pass
    print('Hotel-Webseite: http://127.0.0.1:8000', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
