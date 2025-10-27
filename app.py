import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu
from utils.data_loader import load_workouts
from oldalak import home_page, top_exercises_page, trends_page, heatmap_page, goals_page, achievements_page


class App:
    def __init__(self):
        self.selected_page = None

    def load_data(self):
        st.sidebar.title("🏋️ Workout Analytics")

        if "workout_df" not in st.session_state:
            st.session_state.workout_df = None
        if "demo_mode" not in st.session_state:
            st.session_state.demo_mode = False

        if st.session_state.workout_df is None:
            st.title("📊 Workout Analytics Dashboard")

            uploaded_file = st.file_uploader("",type="csv")
            use_demo = st.button("💾 Demo adat betöltése")

            if uploaded_file:
                st.session_state.workout_df = load_workouts(uploaded_file)
                st.session_state.demo_mode = False
                st.rerun()

            elif use_demo:
                demo_path = os.path.join("data", "example_workout.csv")
                if os.path.exists(demo_path):
                    st.session_state.workout_df = pd.read_csv(demo_path, parse_dates=["start_time", "end_time"])
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

                # 🔹 Újrakezdés gomb
            if st.session_state.get("workout_df") is not None:
                if st.button("🔄 Újrakezdés / adat törlése"):
                    st.session_state.workout_df = None
                    st.session_state.demo_mode = False
                    st.rerun()

            st.write("Created by Jonatan")
            st.markdown(
                "[🌐 Portfolio](https://jehunat.github.io/portfolio)",
                unsafe_allow_html=True
            )

    def render_page(self):
        if self.workout_df is None or self.workout_df.empty:
            st.info("👆 Tölts fel egy CSV fájlt az edzésedről vagy próbáld ki demo adatokkal!")
            return

        if self.selected_page == "Főoldal":
            home_page.render_home(self.workout_df)
        elif self.selected_page == "Top gyakorlatok":
            top_exercises_page.render_top_exercises(self.workout_df)
        elif self.selected_page == "Trendek":
            trends_page.render_trends(self.workout_df)
        elif self.selected_page == "Heatmap":
            heatmap_page.render_heatmap(self.workout_df)
        elif self.selected_page == "Célok / kihívások":
            goals_page.render_goals(self.workout_df)
        elif self.selected_page == "Motiváció / Achievements":
            achievements_page.render_achievements(self.workout_df)

    def run(self):
        st.set_page_config(page_title="Workout Dashboard", layout="wide")
        self.load_data()
        self.show_menu()
        self.render_page()


if __name__ == "__main__":
    app = App()
    app.run()