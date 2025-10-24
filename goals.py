import pandas as pd

def calculate_goal_progress(workout_df, exercise, target_weight, target_reps, target_sets):
    """
    Kiszámolja a célhoz való haladást a legutóbbi edzés alapján.
    Csak a 'normal' szetteket veszi figyelembe.
    """
    # 1. Csak a normál szettek és a kiválasztott gyakorlat
    df = workout_df[
        (workout_df['exercise_title'] == exercise) &
        (workout_df['set_type'] == 'normal')
    ].copy()

    if df.empty:
        return 0.0, 0

    # 2. Utolsó edzés
    last_session_time = df['start_time'].max()
    last_session_df = df[df['start_time'] == last_session_time]

    if last_session_df.empty:
        return 0.0, 0

    # 3. Csak a cél szettet számoljuk
    last_session_df['set_completed'] = ((last_session_df['weight_kg'] >= target_weight) &
                                        (last_session_df['reps'] >= target_reps)).astype(int)
    total_completed_sets = last_session_df['set_completed'].sum()

    # Progressz számítása
    progress = min(total_completed_sets / target_sets, 1.0)
    return progress, total_completed_sets


def get_best_working_sets(workout_df, exercise, top_n_sets=4):
    """
    Visszaadja az utolsó edzésből a legjobb N working szettet (warmup szetteket kihagyva).
    """
    df = workout_df[
        (workout_df['exercise_title'] == exercise) &
        (workout_df['set_type'] == 'normal')
    ].copy()

    if df.empty:
        return pd.DataFrame()

    # Utolsó edzés dátuma
    last_session_time = df['start_time'].max()
    last_session_df = df[df['start_time'] == last_session_time]

    # Súly szerint csökkenő, ismétlés szerint csökkenő sorrendben
    last_session_df = last_session_df.sort_values(by=['weight_kg', 'reps'], ascending=False)

    # Reset index a hibamentes grafikonhoz
    return last_session_df.head(top_n_sets).reset_index(drop=True)
