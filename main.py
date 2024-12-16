import streamlit as st
from random import randint as rand

class Player():
    def __init__(self, name:str):
        self.green = True
        self.pink = True
        self.name = name

def display_game_state_sidebar() -> None:
    """
    Display the current game state in the sidebar
    """
       
    with st.sidebar:
        st.subheader(st.session_state.player_one.name)
        st.image(get_camemberts(st.session_state.player_one), width=40)

def get_camemberts(player: Player):
    result = []
    if player.green:
        result.append("pictures/green_cam.png")
    if player.pink:
        result.append("pictures/pink_cam.png")
    
    return result
        
if "player_one" not in st.session_state:
    st.session_state.player_one = Player("Raouff")
    st.session_state.player_one.green = rand(0,1)
    st.session_state.player_one.pink = rand(0,1)

display_game_state_sidebar()

if st.button("reroll"):
    st.session_state.player_one.green = rand(0,1)
    st.session_state.player_one.pink = rand(0,1)