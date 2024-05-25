import sqlite3

def creare_connessione_database(db_name="database.db"):
    conn = sqlite3.connect(db_name)
    return conn

def verifica_codice_fiscale(conn, codice_fiscale):
    query = "SELECT * FROM Paziente WHERE codice_fiscale = ?"
    cursor = conn.cursor()
    cursor.execute(query, (codice_fiscale,))
    return cursor.fetchone()

def recupera_dati_paziente(conn, codice_fiscale):
    query = "SELECT * FROM Scheda_Paziente WHERE codice_fiscale = ?"
    cursor = conn.cursor()
    cursor.execute(query, (codice_fiscale,))
    return cursor.fetchone()

def inserisci_nuovo_paziente(conn, nuovo_paziente):
    query = """
    INSERT INTO Paziente (nome, cognome, data_nascita, codice_fiscale, comune_di_nascita, residenza)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(query, (nuovo_paziente['nome'], nuovo_paziente['cognome'],
                           nuovo_paziente['data_nascita'], nuovo_paziente['codice_fiscale'],
                           nuovo_paziente['comune_di_nascita'], nuovo_paziente['residenza']))
    conn.commit()
