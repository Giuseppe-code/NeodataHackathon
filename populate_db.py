import sqlite3

# Creare una connessione al database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Query per inserire un nuovo paziente
query_inserisci_paziente = """
INSERT INTO Patient (codice_fiscale, name, surname, birthday, residence, city_of_birth)
VALUES (?, ?, ?, ?, ?, ?)
"""
paziente = ('ABCDEF12G34H567I', 'Mario', 'Rossi', '1980-01-01', 'Via Roma, 1', 'Roma')
cursor.execute(query_inserisci_paziente, paziente)

# Query per inserire la storia clinica del paziente
query_inserisci_storia = """
INSERT INTO Patient_card (codice_fiscale, day_of_registration, symptoms, severity)
VALUES (?, ?, ?, ?)
"""
storia_paziente = [
    ('ABCDEF12G34H567I', '2022-05-01 14:30:00', 'Infarto miocardico acuto', 'red'),
    ('ABCDEF12G34H567I', '2023-01-20 09:00:00', 'Dolore toracico, affanno', 'yellow'),
    ('ABCDEF12G34H567I', '2024-02-10 11:45:00', 'Infarto miocardico acuto', 'red')
]

for record in storia_paziente:
    cursor.execute(query_inserisci_storia, record)

# Salvare le modifiche e chiudere la connessione
conn.commit()
conn.close()
