import questionmodels
import database_utils
import streamlit as st
from enums import Themes
import json_handler

if not "db" in st.session_state:
    st.session_state.db = database_utils.DatabaseUtils()

# questions = json_handler.get_dataset()

# for x in questions:
#     id_question = st.session_state.db.create_question(x["theme"], x["intitule"])
#     for y in range(1, 5):            
#         st.session_state.db.create_answer(id_question, x[f"réponse_{y}"], x[f"bonne_reponse_{y}"])



with st.form("crea_question_form", clear_on_submit=True):
    st.subheader("Intitulé de la question")
    st.text_input("intitulé", key="crea_question_title", label_visibility="collapsed")
    for x in range(1, 5):            
        st.text_input(f"réponse {x}", key=f"crea_question_answer_{x}")
        st.checkbox("bonne réponse?", key=f"crea_good_answer_{x}")
    st.selectbox("Thème :", list(Themes.__members__), index=None, placeholder="Choisir le thème...", key="crea_theme")
    
    
    if st.form_submit_button("Créer"):
        id_question = st.session_state.db.create_question(list(Themes.__members__).index(st.session_state.crea_theme), st.session_state.crea_question_title)
        for x in range(1, 5):            
            st.session_state.db.create_answer(id_question, st.session_state[f"crea_question_answer_{x}"], st.session_state[f"crea_good_answer_{x}"])
        
        