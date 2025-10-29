from datetime import datetime
import pytz
import streamlit as st
from streamlit_calendar import calendar
from analysis import total_workout_time, best_week_streak
from utils.data_loader import get_unique_sessions


def create_calendar(workout_df):
    """ Interactive calendar"""

    st.write("**💡Tipp:** A zöld napokon edzettél.")
    st.write("Kattints egy napra, hogy megnézd az aznapi edzéseidet! 💪")

    workout_days = workout_df['start_time'].dt.date.unique()

    workout_events = []
    for date in workout_df["start_time"].dt.date.unique():
        workout_events.append({
            "start": str(date),
            "display": "background",
            "color": "#7CFC00"
        })

    calendar_options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        "height": 700,
        "firstDay": 1
    }

    state = calendar(
        events=workout_events,
        options=calendar_options,
        custom_css="""
                .fc-toolbar-title {
                    font-size: 24px;
                    font-weight: bold;
                }
            """,
        key="calendar"
    )

    if state.get("dateClick"):
        clicked_date_raw = state["dateClick"]["date"]
        clicked_dt_utc = datetime.fromisoformat(clicked_date_raw.replace("Z", "+00:00"))

        local_tz = pytz.timezone("Europe/Budapest")
        clicked_dt_local = clicked_dt_utc.astimezone(local_tz)
        clicked_date = clicked_dt_local.date()



        workouts_for_day  = workout_df[workout_df['start_time'].dt.date == clicked_date]

        if not workouts_for_day.empty:
            st.write(f"Edzés {clicked_date}-án:")
            for title, group in workouts_for_day.groupby('title'):
                st.write(f"**{title}**")
                st.table(group[['exercise_title', 'weight_kg', 'reps']])
        else:
            st.write("Ezen a napon nem volt edzés.")


def render_home(workout_df):
    st.title("🏋️ Főoldal")

    unique_sessions = get_unique_sessions(workout_df)
    total_hours = total_workout_time(unique_sessions)
    total_workouts = unique_sessions.shape[0]
    first_workout = unique_sessions['start_time'].min().strftime("%Y-%m-%d %H:%M")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⏱ Összes edzésidő", f"{total_hours:.2f} óra")
    col2.metric("🗓 Összes edzés", f"{total_workouts} db")
    col3.metric("🏁 Legelső edzés", f"{first_workout}")
    best_streak = best_week_streak(workout_df, min_days_per_week=4)
    col4.metric("🔥 Best week streak", f"{best_streak} hét")

    st.subheader("Adatok előnézete")
    st.dataframe(workout_df.head(10))

    st.subheader("📅 Edzés Naptár")
    workout_calendar = create_calendar(workout_df)