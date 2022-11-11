"""
Rules for Bayesian Theory of Mind staghunt game!

This is a proof of concept for using streamlit as the ui for this game.
"""

# ---------- Libraries ----------
import streamlit as st

# ------------- Defining Variables -------------

introtext = f"""Dear participant

Thank you for playing against tomsup!
Here we will make you play against simulated agents in the stag hunt game.
If you at any time wish to do so, you are free to stop the experiment and 
ask for any generated data to be deleted. If you have read the above and 
wish to proceed, press 'Next' below."""

rulestext_staghunt = f"""
You will now play a game of staghunt.

You will be a hunter in this game playing with simulated hunters. You can 
choose to hunt either stags or hares. If you and the other hunter(s) both 
go after the stag, you get the greatest payoff. However, if only you go after 
the stag, you get no payoff. If you choose to go after the hares, you will 
get a payoff, but it will be smaller than the payoff for jointly getting the 
stag. Your goal is to maximize your payoff. You must choose whether or not to 
blindly cooperate with the other hunter(s) to get the stag or solely go after 
the hares. But, remember, they may not choose to co-operate with you.

You will play 1 game.
"""

continue_in_terminal = f"""Thank you for participating!

Run main and your game will continue in the terminal.
"""

# ------------- Write intro text -------------

st.header("BToM Stag Hunt")

if "page" not in st.session_state:
    st.session_state.page = 0

def nextpage(): st.session_state.page += 1
def restart(): st.session_state.page = 0

placeholder = st.empty()
placeholder.write(introtext)
st.button("Next",on_click=nextpage)

if st.session_state.page == 1:
    placeholder.write(rulestext_staghunt)

if st.session_state.page == 2:
    # once you have provided this information,
    # stop the streamlit app and continue game in terminal
    placeholder.write(continue_in_terminal)
    st.stop()