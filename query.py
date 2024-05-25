import sqlite3
def creare_connessione_database(db_name="database.db"):
    conn = sqlite3.connect(db_name)
    return conn

#verify the codice fiscale already exixst
def verifica_codice_fiscale(conn, codice_fiscale):
    query = "SELECT * FROM Patient WHERE codice_fiscale = ?"
    cursor = conn.cursor()
    cursor.execute(query, (codice_fiscale,))
    return cursor.fetchone()

#if exists it retrives the data
def recupera_dati_paziente(conn, codice_fiscale):
    query = "SELECT * FROM Patient_card WHERE codice_fiscale = ?"
    cursor = conn.cursor()
    cursor.execute(query, (codice_fiscale,))
    return cursor.fetchone()

#adds the patient if its the first time
def inserisci_nuovo_paziente(conn, nuovo_paziente):
    query = """
    INSERT INTO Patient (codice_fiscale, nome, cognome, data_nascita, indirizzo)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(query, (nuovo_paziente['codice_fiscale'], nuovo_paziente['nome'],
                           nuovo_paziente['cognome'], nuovo_paziente['data_nascita'],
                           nuovo_paziente['indirizzo']))
    conn.commit()