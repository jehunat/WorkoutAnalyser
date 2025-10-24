import streamlit as st
from achievements import get_achievements


def render_achievements(workout_df):
    st.title("🔥 Motiváció és badge-ek")
    badges = get_achievements(workout_df)
    if badges:
        for b in badges:
            st.success(b)
    else:
        st.warning("Még nincsenek badge-jeid — gyerünk edzeni! 💪")

