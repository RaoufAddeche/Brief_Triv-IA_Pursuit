import streamlit as st
from random import randint as rand
from playermodels import Player

def display_game_state_sidebar() -> None:
    """
    Display the current game state in the sidebar
    """
       
    with st.sidebar:
        for player in st.session_state.player_list:
            st.subheader(player.name)
            st.image(get_camemberts(player), width=40)

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
        
if "player_one" not in st.session_state:
    st.session_state.player_one = Player()
    st.session_state.player_one.name = "Raouff"
    st.session_state.player_one.camembert_ACTUALITES_IA = rand(0,1)
    st.session_state.player_one.camembert_BASES_DE_DONNEES = rand(0,1)
    st.session_state.player_one.camembert_DEVOPS = rand(0,1)
    st.session_state.player_one.camembert_LANGAGES_DE_PROGRAMMATION = rand(0,1)
    st.session_state.player_one.camembert_TECH_IA = rand(0,1)
    st.session_state.player_one.camembert_LIGNE_DE_COMMANDES = rand(0,1)
    
    st.session_state.player_two = Player()
    st.session_state.player_two.name = "Victor"
    st.session_state.player_two.camembert_ACTUALITES_IA = rand(0,1)
    st.session_state.player_two.camembert_BASES_DE_DONNEES = rand(0,1)
    st.session_state.player_two.camembert_DEVOPS = rand(0,1)
    st.session_state.player_two.camembert_LANGAGES_DE_PROGRAMMATION = rand(0,1)
    st.session_state.player_two.camembert_TECH_IA = rand(0,1)
    st.session_state.player_two.camembert_LIGNE_DE_COMMANDES = rand(0,1)

    st.session_state.player_three = Player()
    st.session_state.player_three.name = "Nicolas"
    st.session_state.player_three.camembert_ACTUALITES_IA = rand(0,1)
    st.session_state.player_three.camembert_BASES_DE_DONNEES = rand(0,1)
    st.session_state.player_three.camembert_DEVOPS = rand(0,1)
    st.session_state.player_three.camembert_LANGAGES_DE_PROGRAMMATION = rand(0,1)
    st.session_state.player_three.camembert_TECH_IA = rand(0,1)
    st.session_state.player_three.camembert_LIGNE_DE_COMMANDES = rand(0,1)
    
    st.session_state.player_four = Player()
    st.session_state.player_four.name = "Samuel"
    st.session_state.player_four.camembert_ACTUALITES_IA = rand(0,1)
    st.session_state.player_four.camembert_BASES_DE_DONNEES = rand(0,1)
    st.session_state.player_four.camembert_DEVOPS = rand(0,1)
    st.session_state.player_four.camembert_LANGAGES_DE_PROGRAMMATION = rand(0,1)
    st.session_state.player_four.camembert_TECH_IA = rand(0,1)
    st.session_state.player_four.camembert_LIGNE_DE_COMMANDES = rand(0,1)
    
    st.session_state.player_list = []
    st.session_state.player_list.append(st.session_state.player_one)
    st.session_state.player_list.append(st.session_state.player_two)
    st.session_state.player_list.append(st.session_state.player_three)
    st.session_state.player_list.append(st.session_state.player_four)

display_game_state_sidebar()

if st.button("reroll"):
    for player in st.session_state.player_list:
        player.camembert_ACTUALITES_IA = rand(0,1)
        player.camembert_BASES_DE_DONNEES = rand(0,1)
        player.camembert_DEVOPS = rand(0,1)
        player.camembert_LANGAGES_DE_PROGRAMMATION = rand(0,1)
        player.camembert_TECH_IA = rand(0,1)
        player.camembert_LIGNE_DE_COMMANDES = rand(0,1)
