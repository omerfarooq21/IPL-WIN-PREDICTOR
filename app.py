import streamlit as st
import pickle as pt
import pandas as pd
from streamlit_lottie import st_lottie
import json


st.set_page_config('IPL','🏏',layout='centered')
def load_lottie_animation(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)

cx,cy,cz = st.columns([0.3,0.3,0.3])
with cy:
    lottie_animation = load_lottie_animation('./Animation.json')
    st_lottie(lottie_animation, height=200, width=200)


        
model = pt.load(open('ipl.pkl','rb'))
st.title("IPL WIN PREDICTOR")
with st.form("my_form"):
    teams = ['Chennai Super Kings',
    'Delhi Capitals',
    'Gujarat Titans',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad']


    c1,c2 = st.columns([1,1])
    with c1:
        t1 = st.selectbox("Select Batting Team",options=teams)
    teams_copy = teams.copy()  # Make a copy to avoid modifying the original list
    teams_copy.remove(t1)
    with c2:
        t2 = st.selectbox("Select Bowling Team",options=teams_copy)


    # st.error(t1)
    # st.success(t2)
    Target = st.number_input("enter the target",min_value=0)
    c3,c4,c5 = st.columns([1,1,1])
    with c3:
        score = st.number_input("enter the score",min_value=0,step=1)
    with c4:
        overs = st.number_input("enter the over",min_value=0.0, max_value=19.6,step=0.1) 
    with c5:
        wickets = st.number_input("enter the wickets",min_value=0, max_value=10,step=1) 

    if st.form_submit_button('predict'):
        runs_left = Target-score
        balls_left = 120-(overs*6)
        wickets = 10-wickets
        CRR = score/overs
        RRR = (runs_left*6)/balls_left
        input_df = pd.DataFrame(
            {
                'batting_team' :[t1],
                'bowling_team' :[t2],
                'runs_left' :[runs_left],
                'balls_left' :[balls_left],
                'wickets' :[wickets],
                'target_runs' :[Target],
                'CRR' :[CRR],
                'RRR' :[RRR]
            }
        )
        st.table(input_df)
        result = model.predict_proba(input_df)
        st.success(f'{t2} : {round(result[0][0]*100)}')
        st.error(f'{t1} : {round(result[0][1]*100)}')

