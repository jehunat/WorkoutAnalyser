import streamlit as st
from utils.data_loader import get_unique_sessions
from analysis import total_workout_time, best_week_streak
import calendar
from datetime import datetime


def show_colored_workout_calendar(workout_df, year, month):
    month_calendar = calendar.monthcalendar(year, month)
    workout_df['date'] = workout_df['start_time'].dt.date

    st.markdown(f"### {calendar.month_name[month]} {year}")

    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    header_cols = st.columns(7)
    for i, day_name in enumerate(day_names):
        header_cols[i].markdown(f"**{day_name}**")

    for week in month_calendar:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write(" ")  # üres nap
            else:
                day_date = datetime(year, month, day).date()
                day_workouts = workout_df[workout_df['date'] == day_date]

                if not day_workouts.empty:
                    # Edzés intenzitása: összesített súly
                    total_weight = (day_workouts['weight_kg'] * day_workouts['reps']).sum()
                    # Szín: minél nagyobb a súly, annál sötétebb zöld
                    max_weight = workout_df['weight_kg'].max() * workout_df['reps'].max() * 4  # kb skála
                    intensity = min(total_weight / max_weight, 1.0)
                    color = f"rgba(0, 128, 0, {0.3 + 0.7 * intensity})"  # világos-zöld -> sötétzöld

                    if cols[i].button(f"{day}", key=str(day_date), help="Klikkelj az edzés részletekhez"):
                        st.write(f"**Edzések {day_date}:**")
                        for idx, row in day_workouts.iterrows():
                            st.write(
                                f"- {row['title']}: {row['exercise_title']} ({row['reps']}x{row['weight_kg']} kg)")

                    # Színes hátteret a gombhoz
                    cols[i].markdown(
                        f"""<div style='background-color:{color}; padding:10px; border-radius:5px; text-align:center'>{day}</div>""",
                        unsafe_allow_html=True)
                else:
                    cols[i].write(str(day))


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
    today = datetime.today()
    show_colored_workout_calendar(workout_df, today.year, today.month)

    # --- Kattintás az adott napra ---
    clicked_day = st.date_input("Válassz napot részletezéshez:", value=datetime.today().date())
    day_df = workout_df[workout_df['start_time'].dt.date == clicked_day]

    if not day_df.empty:
        st.write(f"Edzések {clicked_day}-án:")
        for title, group in day_df.groupby('title'):
            st.write(f"**{title}**")
            st.table(group[['exercise_title', 'weight_kg', 'reps']])
    else:
        st.write("Ezen a napon nem volt edzés.")