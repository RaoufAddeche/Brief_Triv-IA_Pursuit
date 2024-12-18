import streamlit as st
from playermodels import Player

def display_game_state_sidebar() -> None:
    """
    Display the current game state in the sidebar
    """
    
    with st.sidebar:
        for player in st.session_state.player_list:
            st.subheader(player.name)
            st.image(get_camemberts(player), width=40)
        
        if st.button("DEBUG : Return to game_state 0"):
            st.session_state.game_state = 0
            st.session_state.reset_players = True
            st.rerun()
        
        if st.button("DEBUG : Return to game_state 1"):
            st.session_state.game_state = 1
            st.rerun()

def get_camemberts(player: Player):
    result = []
    if player.camembert_ACTUALITES_IA:
        result.append("pictures/green_cam.png")
    if player.camembert_BASES_DE_DONNEES:
        result.append("pictures/pink_cam.png")
    if player.camembert_DEVOPS:
        result.append("pictures/blue_cam.png")
    if player.camembert_LANGAGES_DE_PROGRAMMATION:
        result.append("pictures/orange_cam.png")
    if player.camembert_LIGNE_DE_COMMANDES:
        result.append("pictures/brown_cam.png")
    if player.camembert_TECH_IA:
        result.append("pictures/yellow_cam.png")
    
    if len(result) == 6:
        return ["pictures/full_wheel.png"]
    
    return result