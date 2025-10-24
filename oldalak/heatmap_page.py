import streamlit as st
from visualization import multi_year_workout_heatmap


def render_heatmap(workout_df):
    st.title("📅 Éves Heatmap")
    figs = multi_year_workout_heatmap(workout_df)
    for fig in figs:
        st.pyplot(fig)
