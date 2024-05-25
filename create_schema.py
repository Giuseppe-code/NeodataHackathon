import sqlite3
import os

# Elimina il file di database esistente se necessario
if os.path.exists('database.db'):
    os.remove('database.db')

# Creare una connessione al database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Creare la tabella Patient
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patient (
        codice_fiscale TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        birthday TEXT NOT NULL,
        residence TEXT NOT NULL,
        city_of_birth TEXT NOT NULL
    );
''')

# Creare la tabella Patient_card
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patient_card (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codice_fiscale TEXT NOT NULL,
        day_of_registration TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        severity TEXT NOT NULL,
        FOREIGN KEY (codice_fiscale) REFERENCES Patient(codice_fiscale)
    );
''')

# Salvare le modifiche e chiudere la connessione
conn.commit()
conn.close()
