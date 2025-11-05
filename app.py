import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from oldalak import home_page, top_exercises_page, trends_page, heatmap_page, goals_page, achievements_page
from utils.data_loader import load_workouts
from utils.ui_helpers import render_intro_text, render_restart_button


class App:
    def __init__(self):
        st.set_page_config(page_title="Workout Dashboard", layout="wide")
        self.workout_df = None
        self.selected_page = None
        self._init_session_state()

    def _init_session_state(self):
        """Initialize session state variables if they don't exist"""
        if "workout_df" not in st.session_state:
            st.session_state.workout_df = None
        if "demo_mode" not in st.session_state:
            st.session_state.demo_mode = False

    def load_data(self):
        """Handle CSV upload and demo data loading"""
        st.sidebar.title("🏋️ Workout Analytics")

        if st.session_state.workout_df is None:
            st.title("📊 Workout Analytics Dashboard")

            uploaded_file = st.file_uploader("",type="csv")
            use_demo = st.button("💾 Demo adat betöltése")

            if uploaded_file:
                st.session_state.workout_df = load_workouts(uploaded_file)
                st.session_state.demo_mode = False
                st.rerun()

            elif use_demo:
                DEMO_FILE_PATH = os.path.join("data", "example_workout.csv")
                if os.path.exists(DEMO_FILE_PATH):
                    st.session_state.workout_df = pd.read_csv(DEMO_FILE_PATH, parse_dates=["start_time", "end_time"])
                    st.session_state.demo_mode = True
                    st.success("✅ Demo adat betöltve!")
                    st.rerun()
                else:
                    st.error("❌ A demo_data.csv fájl nem található.")


        self.workout_df = st.session_state.workout_df


    def show_menu(self):
        with st.sidebar:
            self.selected_page = option_menu(
                menu_title="Navigation",
                options=["Főoldal", "Top gyakorlatok", "Trendek", "Heatmap", "Célok / kihívások", "Motiváció / Achievements"],
                icons=["house-fill", "trophy-fill", "graph-up", "calendar-week-fill", "bullseye", "fire"],
                menu_icon = "cast",
                styles={
                    "container": {"padding": "5!important", "background-color": "black"},
                    "icon": {"color": "orange", "font-size": "23px"},
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

            st.markdown("---")

            if st.session_state.get("demo_mode", False):
                st.info("💾 Demo adat van betöltve")
            elif st.session_state.get("workout_df") is not None:
                st.success("✅ Saját fájl használatban")


            render_restart_button()

            st.markdown("---")
            st.write("Created by Jonatan")
            st.markdown(
                "[🌐 Portfolio](https://jehunat.github.io/portfolio)",
                unsafe_allow_html=True
            )

    def render_page(self):
        """Render the currently selected page"""
        if self.workout_df is None or self.workout_df.empty:
            render_intro_text()
            return

        PAGE_RENDERERS = {
            "Főoldal": home_page.render_home,
            "Top gyakorlatok": top_exercises_page.render_top_exercises,
            "Trendek": trends_page.render_trends,
            "Heatmap": heatmap_page.render_heatmap,
            "Célok / kihívások": goals_page.render_goals,
            "Motiváció / Achievements": achievements_page.render_achievements
        }

        renderer = PAGE_RENDERERS.get(self.selected_page)
        if renderer:
            renderer(self.workout_df)

    def run(self):
        self.load_data()
        self.show_menu()
        self.render_page()


if __name__ == "__main__":
    app = App()
    app.run()