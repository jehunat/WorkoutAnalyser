import streamlit as st
from analysis import top_exercises
from visualization import plot_top_exercises

def render_top_exercises(workout_df):
    st.title("🏆 Top gyakorlatok")
    months = st.slider("Hány hónapot vizsgáljunk?", 1, 12, 3)
    top_n = st.slider("Hány leggyakoribb gyakorlat?", 1, 20, 5)
    top_df = top_exercises(workout_df, months=months, top_n=top_n)
    st.subheader(f"Top {len(top_df)} gyakorlat az elmúlt {months} hónapban")
    st.dataframe(top_df)
    fig = plot_top_exercises(top_df)
    st.pyplot(fig)
