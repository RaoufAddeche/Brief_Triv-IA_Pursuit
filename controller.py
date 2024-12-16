import random

def ask_Questions():

    #organiser les questions par theme
    themes = {}
    for theme, question in questions_data:
        if theme not in themes:
            themes[theme] = []
            themes[theme].append(question)

    #Choix aléatoire des themes

    themes_random = list(themes.key())
    random.shuffle(themes_random)

    #afficher les choix de theme
    print(f"Joueur {joueur}, choissisez un theme :")
    for i, theme in enumerate(themes_random, 1):
        print(f"{i}, {theme}")

    #demander de choisir un theme
    choix= input("Entrez le numéro du thème")
    
    theme_choisi = themes_random[choix - 1]
    question_choisi = themes[theme_choisi][0]

    print(question_choisi)
    reponse = input("votre réponse :")

ask_Questions()