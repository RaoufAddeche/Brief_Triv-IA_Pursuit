import streamlit as st
from playermodels import Player
from enums import Themes

def display_game_state_sidebar() -> None:
    """
    Display the current game state in the sidebar
    """
    
    with st.sidebar:
        x = 0
        for player in st.session_state.player_list:
            if st.session_state.current_player == x:
                st.subheader(f":green[{player.name}]")
            else:
                st.subheader(player.name)
            st.image(get_camemberts(player), width=40)
            x += 1
        
        if st.button("DEBUG : Return to game_state 0"):
            st.session_state.game_state = 0
            st.session_state.reset_game = True
            st.rerun()
        
        if st.button("DEBUG : Return to game_state 1"):
            st.session_state.game_state = 1
            st.rerun()

def get_camemberts(player: Player):
    result = []
    if player.camembert_ACTUALITES_IA:
        result.append("pictures/pink_cam.png")
    if player.camembert_BASES_DE_DONNEES:
        result.append("pictures/orange_cam.png")
    if player.camembert_DEVOPS:
        result.append("pictures/yellow_cam.png")
    if player.camembert_LANGAGES_DE_PROGRAMMATION:
        result.append("pictures/green_cam.png")
    if player.camembert_LIGNE_DE_COMMANDES:
        result.append("pictures/blue_cam.png")
    if player.camembert_TECH_IA:
        result.append("pictures/brown_cam.png")
    
    if len(result) == 6:
        return ["pictures/full_wheel.png"]
    
    return result

def next_player():
    st.session_state.current_player += 1
    if st.session_state.current_player >= len(st.session_state.player_list):
        st.session_state.current_player = 0
        
def current_player():
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