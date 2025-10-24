import streamlit as st
from analysis import  session_volume_analysis, best_set_volume_analysis, total_reps_per_session, heaviest_weight_per_session


def render_trends(workout_df):
    st.title("📈 Gyakorlat Trendek")
    session_volume_analysis(workout_df)
    best_set_volume_analysis(workout_df)
    total_reps_per_session(workout_df)
    heaviest_weight_per_session(workout_df)
