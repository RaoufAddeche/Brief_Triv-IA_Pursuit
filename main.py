import streamlit as st
from random import randint as rand
from playermodels import Player
from streamlit_functions import display_game_state_sidebar, next_player
import database_utils as db
import controller as ctrl
from enums import Themes

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

if st.session_state.reset_game:
    st.session_state.player_count = 1
    st.session_state.player_list = []  
    st.session_state.reset_game = False
    st.session_state.current_player = 0 
    st.session_state.game_step = -1
    
#___________________________

st.write(":red[DEBUG :] game_state = ", st.session_state.game_state)

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
                st.session_state[f"questions_{theme.name}"] = st.session_state.db.get_question_list(theme.value)
            
            st.session_state.game_step = 0
            st.rerun()
        case 0:
            st.header(f"{st.session_state.player_list[st.session_state.current_player].name}, c'est votre tour ! :sunglasses:")
            st.image(f"positions/{st.session_state.player_list[st.session_state.current_player].position_id}.png", caption="Votre position.")
            
            if st.button("joueur suivant"):
                next_player()
                st.rerun()
                      
        
        
        case 1:
            pass
    
        
    # if st.button("DEBUG : Random camemberts"):
    #     for player in st.session_state.player_list:
    #         player.camembert_ACTUALITES_IA = rand(0,1)
    #         player.camembert_BASES_DE_DONNEES = rand(0,1)
    #         player.camembert_DEVOPS = rand(0,1)
    #         player.camembert_LANGAGES_DE_PROGRAMMATION = rand(0,1)
    #         player.camembert_TECH_IA = rand(0,1)
    #         player.camembert_LIGNE_DE_COMMANDES = rand(0,1)
        
    #     st.rerun()
