import streamlit as st
from playermodels import Game, Player
from enums import Themes
from typing import cast
from database_utils import DatabaseUtils
from playermodels import Player
from controller import cheat_get_all_camemberts

def display_game_state_sidebar() -> None:
    """
    Display the current game state in the sidebar
    """
    
    with st.sidebar:
        x = 0
        if st.session_state.game_state == 1:
            st.subheader("Round " + str(st.session_state.current_game.current_round))
        for player in st.session_state.player_list:            
            if st.session_state.current_player == x:
                st.subheader(f":green[{player.name}]")
            else:
                st.subheader(player.name)
            st.image(get_camemberts(player), width=40)
            x += 1
        
        st.divider()
        
        if st.button("DEBUG : Return to game_state 0"):
            st.session_state.game_state = 0
            st.session_state.reset_game = True
            st.rerun()
        
        if st.button("DEBUG : Return to game_state 1"):
            st.session_state.game_state = 1
            st.rerun()
            
        if st.button("DEBUG : 6 :cheese_wedge:"):
            cheat_get_all_camemberts(current_player())
            st.rerun()
            
        if st.button("TEST CENTRE"):
            cheat_test_all_camemberts()

        st.divider()

        if st.session_state.get("game_state") == 1 :
            if st.button("Sauver cette partie"):
                current_game  = st.session_state.get("current_game")
                player_list  = st.session_state.get("player_list")
                if current_game != None and player_list != None :
                    # st.write("current game = ")
                    # st.write(current_game)
                    # st.write(player_list)

                    current_game = cast(Game, current_game)
                
                    player_list = cast(list[Player], player_list)
                    current_game.players = player_list
                   
                    actual_player = current_player()

                    actual_player = cast(Player, actual_player)
                    current_game.current_player_id = actual_player.id_player

                    db_methods = DatabaseUtils()
                    db_methods.update_game(current_game)

        if st.button("Charger une partie"):
            st.session_state["load_game_mode"] = True
            st.rerun()

        if st.session_state.get("load_game_mode") == True :
            db_methods = DatabaseUtils()
            games = db_methods.get_game_list()
            options_ids = {}
            options_ids[""] = -1
            for game in games :
                option = game.date.strftime("%d %b %Y")
                option += " :"
                for player in game.players :
                    option += " " +player.name

                options_ids[option] = game.id_game

            selected_option = st.selectbox("Laquelle ?", options_ids)
            selected_game_id = options_ids[selected_option]
            if selected_game_id != -1 :
                st.session_state["load_game_mode"] = False 
                selected_game = next(filter(lambda g : g.id_game == selected_game_id, games))
                selected_game = cast(Game, selected_game)
                #st.write(selected_game)
                st.session_state["current_game"] = selected_game
                n = len(selected_game.players)
                st.session_state["player_count"] = n
                player_list = []
                selected_player_index = 0 # if no selection, the first one
                for i in range(0,n) :
                    loop_player = selected_game.players[i]
                    st.session_state[f"player_{i}"] = loop_player
                    player_list.append(loop_player)
                    if loop_player.id_player == selected_game.current_player_id :
                        selected_player_index = i

                st.session_state["player_list"] = player_list
                st.session_state["current_player"] = selected_player_index
                st.session_state["game_state"] = 1
                st.session_state["game_step"] = -1
                st.rerun()                    
                

                    
                    

def get_camemberts(player: Player):
    result = []
    if player.camembert_ACTUALITES_IA:
        result.append("pictures/violet_cam.png")
    if player.camembert_BASES_DE_DONNEES:
        result.append("pictures/orange_cam.png")
    if player.camembert_DEVOPS:
        result.append("pictures/red_cam.png")
    if player.camembert_LANGAGES_DE_PROGRAMMATION:
        result.append("pictures/green_cam.png")
    if player.camembert_LIGNE_DE_COMMANDES:
        result.append("pictures/blue_cam.png")
    if player.camembert_TECH_IA:
        result.append("pictures/rainbow_cam.png")
    
    if len(result) == 6:
        return ["pictures/full_wheel.png"]
    
    return result

def next_player():
    st.session_state.current_player += 1
    if st.session_state.current_player >= len(st.session_state.player_list):
        st.session_state.current_player = 0
        st.session_state.current_game.current_round += 1
        
def current_player() -> Player:
    return st.session_state[f"player_{st.session_state.current_player}"]

def return_dice_outcomes():
    result = []
    
    result.append(return_theme_string(st.session_state.current_moves[0].theme))
    if st.session_state.current_moves[0].iscamembert:
        result[0] = result[0] + " ==> :green[:cheese_wedge: CAMEMBERT !]"
    result.append(return_theme_string(st.session_state.current_moves[1].theme))
    if st.session_state.current_moves[1].iscamembert:
        result[1] = result[1] + " ==> :green[:cheese_wedge: CAMEMBERT !]"
    
    return result
    
def return_theme_string(theme_id):
    match theme_id:
        case 0:
            return ":orange[Base de Données]"
        case 1:
            return ":green[Langage de Programmation : Python]"
        case 2:
            return ":blue[Lignes de Commandes Unix]"
        case 3:
            return ":violet[Actualité IA]"
        case 4:
            return ":red[DevOps]"
        case 5:
            return ":rainbow[Tech IA 6]"
        case 6:
            return "Relance !"
    
def cheat_test_all_camemberts():
    cheat_get_all_camemberts(current_player())
    current_player().camembert_BASES_DE_DONNEES = False
    current_player().position_id = 1
    st.session_state.game_step = 0
    st.rerun()