import streamlit as st
from random import randint, shuffle
from playermodels import Player
from streamlit_functions import display_game_state_sidebar, next_player, current_player, return_dice_outcomes
import database_utils as db
import controller as ctrl
from enums import Themes
import time
from positions import create_all_position, create_center_position

#region Init
#Intialization and script resets
#___________________________
if "game_state" not in st.session_state:
    #game_state = 0 : players choice
    #game_state = 1 : game play
    st.session_state.game_state = 0    
    #game_step = -1 : initialization
    #game_step = 0 : before throw die or next playe
    #game_step = 1 : choose direction
    #game_step = 2 : show question
    #game_step = 3 : correct answer
    #game_step = 4 : bad arect answer  
    #game_step = 5 : final test 
    #game_step = 6 : final test is valid
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
    st.session_state.center_board = create_center_position()
    
    st.session_state.create_final_test = False
    st.session_state.final_test_questions = []
    st.session_state.final_test_questions_answers_texts = []

if st.session_state.reset_game:
    st.session_state.player_count = 1
    st.session_state.player_list = []  
    st.session_state.reset_game = False
    st.session_state.current_player = 0 
    st.session_state.game_step = -1
    st.session_state.create_final_test = False
    st.session_state.final_test_questions = []
    st.session_state.final_test_questions_answers_texts = []
    
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
            st.session_state.current_game = st.session_state.db.get_game(id_game)
            
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
            st.image(f"positions/{current_player().position_id}.png", caption="Votre position.", width=350)
            
            if current_player().position_id == 99:
                if st.button(":green[Test final !]"):
                    st.session_state.game_step = 5
                    st.session_state.create_final_test = True
                    st.rerun()
            
            elif current_player().is_final_step():
                if st.button("Case suivante"):
                    st.session_state.game_step = 2
                    pos = ctrl.streamlit_found_diag_position(current_player(), st.session_state.board, st.session_state.center_board)
                    st.session_state.current_question_index = randint(0, len(st.session_state[f"questions_{pos.theme}"])-1)
                    st.session_state.current_question = st.session_state[f"questions_{pos.theme}"][st.session_state.current_question_index]
                    st.session_state[f"questions_{pos.theme}"].pop(st.session_state.current_question_index)
                    if len(st.session_state[f"questions_{pos.theme}"]) == 0:
                        st.session_state[f"questions_{pos.theme}"] = st.session_state.db.get_question_list(pos.theme)
                    st.rerun()
            else:
                if st.session_state.dice_anim:                     
                    while True:
                        r = randint(1,1)
                        st.session_state.last_dice_frame = 1
                        break
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
            
            radio_answers = st.radio("radio", answer_texts, label_visibility="collapsed")
                        
            if st.button("Valider la réponse"):
                if st.session_state.current_question.answers[answer_texts.index(radio_answers)].is_correct :
                    current_player().num_of_questions_with_correct_answer += 1
                    if st.session_state.current_pos.iscamembert and not current_player().is_final_step():
                        ctrl.update_camembert(current_player(), st.session_state.current_pos.theme)
                        st.session_state.balloons = True
                    if current_player().is_final_step and current_player().position_id > 41:
                        position = ctrl.streamlit_found_diag_position(current_player(), st.session_state.board, st.session_state.center_board)
                        new_position = position.move_to_win()
                        current_player().position_id = new_position
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
                if current_player().is_final_step() and current_player().position_id <= 41:
                    st.write()
                    st.write(f"Bravo, :green[{current_player().name}], vous avez obtenu tous les camemberts ! :cheese_wedge: ")
                    current_player().position_id = st.session_state.center_board[int(current_player().position_id/7)][0].id
            if st.button("Rejouer."):
                st.session_state.game_step = 0
                st.rerun()
        
        case 4 :
            st.write(":red[Mauvaise réponse !]")
            if st.button("Joueur suivant."):
                st.session_state.game_step = 0
                next_player()
                st.rerun()
        
        case 5:
            if st.session_state.create_final_test:
                st.session_state.create_final_test = False
                st.session_state.final_test_questions = []
                
                for x in range (0, 6):
                    st.session_state.current_question_index = randint(0, len(st.session_state[f"questions_{x}"])-1)
                    question = st.session_state[f"questions_{x}"][st.session_state.current_question_index]
                    st.session_state[f"questions_{x}"].pop(st.session_state.current_question_index)
                    if len(st.session_state[f"questions_{x}"]) == 0:
                        st.session_state[f"questions_{x}"] = st.session_state.db.get_question_list(x)
                    st.session_state.final_test_questions.append(question)
                    st.session_state.final_test_questions_answers_texts.append([i.text for i in question.answers])
            
            x = 0
            for question in st.session_state.final_test_questions:
                st.header(question.text)
                
                st.radio("", st.session_state.final_test_questions_answers_texts[x], key=f"final_answers_{x}")
                
                st.divider()
                
                x+=1
                            
            if st.button("Valider les réponses"):
                is_won = True
                for x in range(0, 6):
                    if not st.session_state.final_test_questions[x].answers[st.session_state.final_test_questions_answers_texts[x].index(st.session_state[f"final_answers_{x}"])].is_correct :
                        is_won = False
                        current_player().num_of_questions_with_bad_answer += 1
                        break
                    else:
                        current_player().num_of_questions_with_correct_answer += 1
                
                if is_won:
                    st.session_state.game_step = 6
                else:
                    st.session_state.game_step = 4
                
                
                st.rerun()
        
        case 6:
           st.balloons()
           st.header(f"BRAVO :green[{current_player().name}], C'EST GAGNE !!")
           st.image("pictures/lepers_ouioui.gif")
           st.audio("sounds/lepers_ouioui.mp3", autoplay=True)
           st.session_state.game_state = 2

#region Game State 2
if st.session_state.game_state == 2:
    st.header("RESULTATS DE LA PARTIE")
           
                
            
