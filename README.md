## Langchain Chatbot With GPT4O Model

## Descrizione del Progetto

Questo progetto è stato sviluppato per l'hackathon di Neodata. Si tratta di un chatbot avanzato che utilizza il modello LLAMA3- e il framework Langchain per analizzare la condizione dei pazienti e categorizzare la gravità della loro condizione in base ai dettagli forniti.

## Componenti del Team

- Giuseppe Vinci
- Giuseppe Stancanelli
- Valerio Messina

## Funzionalità Principali

- **Categorizzazione della Gravità**: Il chatbot risponde con "verde", "giallo" o "rosso" per indicare la gravità della condizione del paziente.
- **Estrazione dei Dettagli del Paziente**: Il chatbot è in grado di estrarre dettagli strutturati dal testo fornito, come Nome, Cognome, Data di Nascita, Genere, Localizzazione, Segni Vitali e Sintomi.
- **Generazione di Report LaTeX**: Il sistema genera un report in formato LaTeX con i dettagli del paziente e la categorizzazione della gravità.
- **Simulato** il workflow di conversazione tra l'operatore di traige, medico specialista e medico generale.

## Utilizzo

### Installazione

1. Clona la repository:
   ```bash
   git clone [https://github.com/tuo-username/tuo-repository.git](https://github.com/Giuseppe-code/NeodataHackathon.git)
2. Installa le dipendenze
    ```bash
    pip install -r requirements.txt
3. Avvia l'applicazione con
   ```bash
   streamlit run chatbot.py
4. Nota: Prima di scrivere qualsiasi messaggio caricare su tutte le pagine per caricare le sessioni
   
