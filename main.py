import streamlit as st
from random import randint, shuffle
from playermodels import Player
from streamlit_functions import display_game_state_sidebar, next_player, current_player, return_dice_outcomes
import database_utils as db
import controller as ctrl
from enums import Themes
import time
from positions import create_all_position

#region Init
#Intialization and script resets
#___________________________
if "game_state" not in st.session_state:
    st.session_state.game_state = 0    
    st.session_state.game_step = -1
    st.session_state.player_count = 1     
    st.session_state.current_player = 0 
    
    st.session_state.player_list = []  

    st.session_state.reset_game = False
    
    st.session_state.db = db.DatabaseUtils()
    
    st.session_state.dice_anim = False
    st.session_state.timer = 0
    st.session_state.last_dice_frame = 0
    st.session_state.balloons = False
    
    st.session_state.dice_outcomes = []
    st.session_state.current_question = None
    
    st.session_state.board = create_all_position()

if st.session_state.reset_game:
    st.session_state.player_count = 1
    st.session_state.player_list = []  
    st.session_state.reset_game = False
    st.session_state.current_player = 0 
    st.session_state.game_step = -1
    
#___________________________

st.write(":red[DEBUG :] game_state = ", st.session_state.game_state)
st.write(":red[DEBUG :] game_step = ", st.session_state.game_step)

st.title(":rainbow[Triv-IA] Pursuit")

#region Game State 0 
#Start of a new game
if st.session_state.game_state == 0:
    st.header("Nouvelle partie :")
    
    #Display textinput for each player with a button to add new players.
    for x in range(0, st.session_state.player_count):
        st.text_input(f"Joueur {x+1} :", key=f"player_name_{x}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.player_count < 6:
            if st.button("Ajouter un joueur"):      
                st.session_state.player_count += 1
                st.rerun()
    with col2:
        if st.session_state.player_count > 0 : 
            if st.button("Retirer dernier joueur"):
                st.session_state.player_count -= 1
                st.rerun()
    
    st.divider()
    
    #Add all current players to the player pool and start the game
    if st.button("Lancer le jeu"):
        
        #Make sure no textinput are empty. If one or more is, display an error.
        name_validation = True
        for x in range(0, st.session_state.player_count):
            if st.session_state[f"player_name_{x}"].strip() == "" or st.session_state[f"player_name_{x}"] == None:
                st.error(f"Joueur {x+1} n'a pas de nom !")
                name_validation = False
                break
        
        #If all name are valid, add players to the pool and launch the game. 
        if name_validation:
            
            id_game = st.session_state.db.create_game()
            st.session_state.game_id = id_game
            
            for x in range(0, st.session_state.player_count):
                st.session_state[f"player_{x}"] = st.session_state.db.create_player(id_game, st.session_state[f"player_name_{x}"])
                st.session_state[f"player_{x}"].position_id = (x*7)
                st.session_state.player_list.append(st.session_state[f"player_{x}"])
            
            st.session_state.game_state = 1
            st.rerun()
   

display_game_state_sidebar()

#region Game State 1


if st.session_state.game_state == 1:
    match st.session_state.game_step:
        case -1:
            for theme in Themes:
                st.session_state[f"questions_{theme.value}"] = st.session_state.db.get_question_list(theme.value)
                for question in st.session_state[f"questions_{theme.value}"]:
                    shuffle(question.answers)
                
            st.session_state.game_step = 0
            st.rerun()
        case 0:
            st.header(f":green[{st.session_state.player_list[st.session_state.current_player].name}], c'est votre tour ! :sunglasses:")
            st.image(f"positions/{st.session_state.player_list[st.session_state.current_player].position_id}.png", caption="Votre position.", width=350)
            
            if st.session_state.dice_anim:                     
                while True:
                    r = randint(1,6)
                    if r != st.session_state.last_dice_frame:
                        st.session_state.last_dice_frame = r
                        break
                st.image(f"pictures/dice/{st.session_state.last_dice_frame}.png")
                time.sleep(0.12)
                st.session_state.timer -= 1
                if st.session_state.timer <= 0:
                    st.session_state.dice_anim = False
                    st.session_state.game_step = 1
                    st.session_state.dice_outcomes = ctrl.get_possible_move(st.session_state.board[current_player().position_id], st.session_state.last_dice_frame)
                    st.session_state.current_moves = [st.session_state.board[st.session_state.dice_outcomes[0]], st.session_state.board[st.session_state.dice_outcomes[1]]]
                st.rerun()                  
            else:                
                if st.button("Lancer le dé"):
                    st.audio("sounds/dice_roll.mp3",autoplay=True,)
                    st.session_state.dice_anim = True
                    st.session_state.timer = 10 
                    st.rerun()  
      
        case 1:
            st.header(f":green[{st.session_state.player_list[st.session_state.current_player].name}], faites votre choix ! :game_die:")
            st.image(f"positions/{st.session_state.player_list[st.session_state.current_player].position_id}.png", caption="Votre position.", width=350)
            st.image(f"pictures/dice/{st.session_state.last_dice_frame}.png")
            
            options = return_dice_outcomes()
            
            radio_choice = st.radio("Faites votre choix :", options)
            
            if st.button("Valider"):
                if radio_choice == "Relance !":
                    st.session_state.game_step = 0
                    current_player().position_id = st.session_state.dice_outcomes[options.index(radio_choice)]
                    st.rerun()
                else:                    
                    if options.index(radio_choice) == 0:
                        st.session_state.current_question_index = randint(0, len(st.session_state[f"questions_{st.session_state.current_moves[0].theme}"])-1)
                        st.session_state.current_question = st.session_state[f"questions_{st.session_state.current_moves[0].theme}"][st.session_state.current_question_index]
                        st.session_state[f"questions_{st.session_state.current_moves[0].theme}"].pop(st.session_state.current_question_index)
                        if len(st.session_state[f"questions_{st.session_state.current_moves[0].theme}"]) == 0:
                            st.session_state[f"questions_{st.session_state.current_moves[0].theme}"] = st.session_state.db.get_question_list(st.session_state.current_moves[0].theme)
                        current_player().position_id = st.session_state.dice_outcomes[0]
                        st.session_state.current_pos = st.session_state.board[st.session_state.dice_outcomes[0]]
                    else:
                        st.session_state.current_question_index = randint(0, len(st.session_state[f"questions_{st.session_state.current_moves[1].theme}"])-1)
                        st.session_state.current_question = st.session_state[f"questions_{st.session_state.current_moves[1].theme}"][st.session_state.current_question_index]
                        st.session_state[f"questions_{st.session_state.current_moves[1].theme}"].pop(st.session_state.current_question_index)
                        if len(st.session_state[f"questions_{st.session_state.current_moves[1].theme}"]) == 0:
                            st.session_state[f"questions_{st.session_state.current_moves[1].theme}"] = st.session_state.db.get_question_list(st.session_state.current_moves[1].theme)
                        current_player().position_id = st.session_state.dice_outcomes[1]
                        st.session_state.current_pos = st.session_state.board[st.session_state.dice_outcomes[1]]
                    st.session_state.game_step = 2
                    st.rerun()
        
        case 2:
            st.header(st.session_state.current_question.text)
            
            answer_texts = [i.text for i in st.session_state.current_question.answers]
            
            radio_answers = st.radio("", answer_texts)
                        
            if st.button("Valider la réponse"):
                if st.session_state.current_question.answers[answer_texts.index(radio_answers)].is_correct :
                    current_player().num_of_questions_with_correct_answer += 1
                    if st.session_state.current_pos.iscamembert:
                        ctrl.update_camembert(current_player(), st.session_state.current_pos.theme)
                        st.session_state.balloons = True
                    st.session_state.game_step = 3
                else:
                    current_player().num_of_questions_with_bad_answer += 1
                    st.session_state.game_step = 4
                
                
                st.rerun()
        
        case 3 :
            st.write(":green[Bonne réponse !]")
            if st.session_state.balloons:
                st.session_state.balloons = False
                st.balloons()
            if st.button("Rejouer."):
                st.session_state.game_step = 0
                st.rerun()
        
        case 4 :
            st.write(":red[Mauvaise réponse !]")
            if st.button("Joueur suivant."):
                st.session_state.game_step = 0
                next_player()
                st.rerun()
           
                
            
