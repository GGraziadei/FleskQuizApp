from app import Option, Quiz, db, app

quizzes_data = [
    {
        'question': 'Qual è un vantaggio dell\'utilizzo di Python per lo sviluppo di intelligenza artificiale?',
        'options': ['Sintassi chiara e leggibile', 'Alto consumo di risorse', 'Difficoltà nell\'installazione di librerie', 'Mancanza di comunità di supporto'],
        'correct_option': 0,
    },
    {
        'question': 'Cos\'è il machine learning?',
        'options': ['Un tipo di caffè', 'Un metodo per insegnare alle macchine a imparare dai dati', 'Un linguaggio di programmazione', 'Un sistema operativo'],
        'correct_option': 1,
    },
    {
        'question': 'In che modo il deep learning è diverso dal machine learning tradizionale?',
        'options': ['Non ci sono differenze', 'Il deep learning coinvolge reti neurali profonde', 'Il machine learning tradizionale utilizza algoritmi più complessi', 'Il deep learning utilizza solo dati strutturati'],
        'correct_option': 1,
    },
    {
        'question': 'Cosa rappresenta l\'acronimo CNN nella visione computerizzata?',
        'options': ['Computerized Neural Network', 'Categorical Neural Network', 'Convolutional Neural Network', 'Compact Neural Network'],
        'correct_option': 2,
    },
    {
        'question': 'Qual è uno dei principali usi della visione computerizzata?',
        'options': ['Creare grafici e tabelle', 'Riconoscimento di pattern e oggetti nelle immagini', 'Tradurre testi da una lingua all\'altra', 'Calcolare la precisione matematica'],
        'correct_option': 1,
    },
    {
        'question': 'Cosa rappresenta l\'acronimo NLP?',
        'options': ['Natural Language Processing', 'New Learning Protocol', 'Neural Linguistic Programming', 'Nonlinear Language Processor'],
        'correct_option': 0,
    },
    {
        'question': 'In che modo l\'NLP è utilizzato nelle applicazioni Python?',
        'options': ['Per creare grafici e visualizzazioni', 'Per eseguire calcoli matematici', 'Per analizzare e manipolare il linguaggio naturale', 'Per giocare a giochi online'],
        'correct_option': 2,
    },
    {
        'question': 'Cosa rappresenta l\'acronimo AI?',
        'options': ['Artificial Intelligence', 'Advanced Internet', 'Automated Integration', 'Active Interface'],
        'correct_option': 0,
    },
    {
        'question': 'Qual è uno dei vantaggi dell\'utilizzo di modelli di intelligenza artificiale nelle applicazioni Python?',
        'options': ['Aumentare la velocità del computer', 'Rendere il codice più breve', 'Aggiungere effetti grafici', 'Migliorare l\'elaborazione dei dati'],
        'correct_option': 3,
    },
]

with app.app_context():
    for quiz_data in quizzes_data:
        quiz = Quiz(text=quiz_data['question'])
        db.session.add(quiz)
        db.session.commit()

        for i, option_text in enumerate(quiz_data['options']):
            is_correct = i == quiz_data['correct_option']
            option = Option(text=option_text, correct=is_correct, quiz=quiz)
            db.session.add(option)
            db.session.commit()
