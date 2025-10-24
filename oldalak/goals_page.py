import streamlit as st
from goals import calculate_goal_progress, get_best_working_sets
from  visualization import plot_goal_progress_sets


def render_goals(workout_df):
    st.title("🎯 Célok / kihívások")
    exercise_goal = st.selectbox("Válassz gyakorlatot a célhoz:", workout_df['exercise_title'].unique())
    target_weight = st.number_input("Cél súly (kg):", min_value=0.0, value=100.0)
    target_reps = st.number_input("Cél ismétlés:", min_value=1, value=10)
    target_sets = st.number_input("Cél szettek száma:", min_value=1, value=4)

    progress, completed_sets = calculate_goal_progress(
        workout_df, exercise_goal, target_weight, target_reps, target_sets
    )
    st.metric(label="Teljesített szettek", value=f"{completed_sets}/{target_sets}")
    st.progress(progress)
    st.write(f"A célhoz való haladás: {progress * 100:.1f}%")

    best_sets = get_best_working_sets(workout_df, exercise_goal, top_n_sets=target_sets)
    st.subheader(f"Legjobb {target_sets} working szetted a legutóbbi edzésből")
    fig_sets = plot_goal_progress_sets(best_sets, exercise_goal)
    st.pyplot(fig_sets)
