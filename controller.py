import random


# Données des questions
questions_data = [
    ("Histoire", "Quel est le nom du roi qui a construit Versailles ?"),
    ("Histoire", "Quelle année a marqué la Révolution française ?"),
    ("Science", "Quel est l'élément chimique symbolisé par 'O' ?"),
    ("Science", "Quelle est la planète la plus proche du Soleil ?"),
    ("Géographie", "Quel est le plus grand désert du monde ?"),
    ("Géographie", "Quelle est la capitale du Canada ?")
]

# Fonction pour organiser les questions par thème
def questions_by_theme():
    themes = []
    for theme, question in questions_data:
        for t in themes:
            if t['theme'] == theme:
                t['questions'].append(question)
                break
        else:
            themes.append({'theme' : theme, 'questions' : [question]})
    return themes


# Fonction principale du jeu
def ask_Questions():
    themes = questions_by_theme()
    joueurs = ["Joueur 1", "Joueur 2"]
    current_joueur = 0


    while True:

        print(f"C'est au tour de {joueurs[current_joueur]}")

        #Choix aléatoire de 2 themes
        themes_random = random.sample(themes,2)
        print("choissisez un theme :")
        for i, theme in enumerate(themes_random, 1):
            print(f"{i}, {theme}")

        #demander de choisir un theme
        choix= int(input("Entrez le numéro du thème"))
        while choix not in [1,2]:
            choix = int(input("choix invalide"))
        
        theme_choisi = themes_random[choix - 1]
        question_choisie = random.choice(theme_choisi["questions"])
        print(question_choisie)


        reponse = input("votre réponse :")

        #si reponse correcte le joueur continue, sinon joueur suivant
        reponse_correcte = "reponse"
        if reponse == reponse_correcte:
            print("bonne reponse ! question suivante")

        else:
            print("mauvaise reponse")
            current_joueur= (current_joueur +1)%2

ask_Questions()