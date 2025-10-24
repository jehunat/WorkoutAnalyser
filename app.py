import streamlit as st
from streamlit_option_menu import option_menu
from data_loader import load_workouts
from oldalak import home_page, top_exercises_page, trends_page, heatmap_page, goals_page, achievements_page


class App:
    def __init__(self):
        self.workout_df = None
        self.selected_page = None

    def load_data(self):
        uploaded_file = st.file_uploader("Töltsd fel az edzés CSV fájlodat", type="csv")
        if uploaded_file:
            self.workout_df = load_workouts(uploaded_file)

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

    def render_page(self):
        if self.workout_df is None or self.workout_df.empty:
            st.info("Kérlek töltsd fel a CSV fájlodat a megjelenítéshez.")
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