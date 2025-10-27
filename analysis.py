import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def total_workout_time(unique_sessions: pd.DataFrame) -> float:
    """Összesített edzésidő órában."""
    total_duration = unique_sessions['duration'].sum()
    total_hours = total_duration.total_seconds() / 3600
    return total_hours

def top_exercises(df: pd.DataFrame, months: int = 3, top_n: int = 5, datetime_col='start_time', exercise_col='exercise_title') -> pd.DataFrame:
    """
    Visszaadja az elmúlt `months` hónapban a `top_n` leggyakoribb gyakorlatot.
    Egy edzésen egyszer számít, ha többször előfordul.
    """
    df = df.copy()
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
    df = df.dropna(subset=[datetime_col, exercise_col])

    cutoff = pd.Timestamp.now() - pd.DateOffset(months=months)
    df = df[df[datetime_col] >= cutoff]

    if df.empty:
        return pd.DataFrame(columns=[exercise_col, 'sessions_count'])

    df['session_id'] = df[datetime_col].dt.strftime('%Y-%m-%d %H:%M:%S')
    unique_pairs = df[[exercise_col, 'session_id']].drop_duplicates()

    counts = (
        unique_pairs.groupby(exercise_col)
        .size()
        .rename('sessions_count')
        .reset_index()
        .sort_values(by='sessions_count', ascending=False)
        .reset_index(drop=True)
    )

    top_n = min(top_n, len(counts))
    return counts.head(top_n)

def calculate_streak(df):
    """Kiszámítja hány napja van folyamatosan aktív streak."""
    df = df.sort_values("start_time")
    unique_days = sorted(df["start_time"].dt.normalize().unique())
    streak = 1
    max_streak = 1
    for i in range(1, len(unique_days)):
        if (unique_days[i] - unique_days[i - 1]).days == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1
    return max_streak

def calculate_weekly_streak(df, min_workouts_per_week=4):
    """
    Hány héten keresztül teljesítettük legalább `min_workouts_per_week` edzést egymás után.
    """
    df = df.dropna(subset=['start_time']).copy()
    df['week'] = df['start_time'].dt.isocalendar().week
    df['year'] = df['start_time'].dt.isocalendar().year

    week_counts = df.groupby(['year', 'week']).size().sort_index()
    streak = 0
    max_streak = 0

    for count in week_counts:
        if count >= min_workouts_per_week:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0

    return streak


def session_volume_analysis(workout_df):
    st.subheader("📊 Gyakorlat Session Volumen Statisztika")

    exercise_list = workout_df['exercise_title'].unique()
    selected_exercise = st.selectbox("Válassz gyakorlatot:", exercise_list)

    period_option = st.radio("Időszak:", ["Elmúlt 3 hónap", "Elmúlt 1 év", "Minden idő"])
    now = pd.Timestamp.now()

    if period_option == "Elmúlt 3 hónap":
        cutoff = now - pd.DateOffset(months=3)
    elif period_option == "Elmúlt 1 év":
        cutoff = now - pd.DateOffset(years=1)
    else:
        cutoff = pd.Timestamp.min

    # Csak a kiválasztott gyakorlat és normál szettek
    df = workout_df[
        (workout_df['exercise_title'] == selected_exercise) &
        (workout_df['set_type'] == 'normal') &
        (workout_df['start_time'] >= cutoff)
        ].copy()

    if df.empty:
        st.warning("Nincs adat a kiválasztott gyakorlatra ebben az időszakban.")
        return

    # Session ID: minden edzés egyedi dátum/idő
    df['session_id'] = df['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Session volumen = összes súly × ismétlés egy edzésen
    session_volume = df.groupby('session_id').apply(lambda x: (x['weight_kg'] * x['reps']).sum())
    session_volume = session_volume.sort_index()

    # Diagram
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(session_volume.index, session_volume.values, color='skyblue', edgecolor='black')
    ax.set_xlabel("Edzés dátuma")
    ax.set_ylabel("Session volumen (kg×reps)")
    ax.set_title(f"{selected_exercise} – Session volumen")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)


def heaviest_weight_per_session(workout_df):
    st.subheader("🏋️‍♂️ Heaviest weight sessionenként (warmup kizárva)")

    exercise_list = workout_df['exercise_title'].unique()
    selected_exercise = st.selectbox("Válassz gyakorlatot a heaviest weight diagramhoz:", exercise_list, key="heaviest_weight_exercise")

    period_option = st.radio("Időszak:", ["Elmúlt 3 hónap", "Elmúlt 1 év", "Minden idő"], key="heaviest_weight_period")
    now = pd.Timestamp.now()

    if period_option == "Elmúlt 3 hónap":
        cutoff = now - pd.DateOffset(months=3)
    elif period_option == "Elmúlt 1 év":
        cutoff = now - pd.DateOffset(years=1)
    else:
        cutoff = pd.Timestamp.min

    # Warmup szettek kizárása
    df = workout_df[
        (workout_df['exercise_title'] == selected_exercise) &
        (workout_df['set_type'] != 'warmup') &
        (workout_df['start_time'] >= cutoff)
    ].copy()

    if df.empty:
        st.warning("Nincs adat a kiválasztott gyakorlatra ebben az időszakban.")
        return

    df['session_id'] = df['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    heaviest = df.groupby('session_id')['weight_kg'].max().sort_index()

    # Diagram
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(heaviest.index, heaviest.values, color='salmon', edgecolor='black')

    # Oszlopok tetejére szöveg
    for bar, value in zip(bars, heaviest.values):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.5, f"{value} kg", ha='center', va='bottom', fontsize=9)

    ax.set_xlabel("Edzés dátuma")
    ax.set_ylabel("Legnehezebb súly (kg)")
    ax.set_title(f"{selected_exercise} – Heaviest weight sessionenként")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)


def total_reps_per_session(workout_df):
    st.subheader("🏋️‍♂️ Összes ismétlés sessionenként (warmup kizárva)")

    exercise_list = workout_df['exercise_title'].unique()
    selected_exercise = st.selectbox("Válassz gyakorlatot a total reps diagramhoz:", exercise_list, key="total_reps_exercise")

    period_option = st.radio("Időszak:", ["Elmúlt 3 hónap", "Elmúlt 1 év", "Minden idő"], key="total_reps_period")
    now = pd.Timestamp.now()

    if period_option == "Elmúlt 3 hónap":
        cutoff = now - pd.DateOffset(months=3)
    elif period_option == "Elmúlt 1 év":
        cutoff = now - pd.DateOffset(years=1)
    else:
        cutoff = pd.Timestamp.min

    # Warmup szettek kizárása
    df = workout_df[
        (workout_df['exercise_title'] == selected_exercise) &
        (workout_df['set_type'] != 'warmup') &
        (workout_df['start_time'] >= cutoff)
    ].copy()

    if df.empty:
        st.warning("Nincs adat a kiválasztott gyakorlatra ebben az időszakban.")
        return

    df['session_id'] = df['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    total_reps = df.groupby('session_id')['reps'].sum().sort_index()

    # Diagram
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(total_reps.index, total_reps.values, color='lightgreen', edgecolor='black')

    # Oszlopok tetejére szöveg
    for bar, value in zip(bars, total_reps.values):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.5, f"{value}", ha='center', va='bottom', fontsize=9)

    ax.set_xlabel("Edzés dátuma")
    ax.set_ylabel("Összes ismétlés")
    ax.set_title(f"{selected_exercise} – Total reps sessionenként")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)


def best_set_volume_analysis(workout_df):
    st.subheader("🏋️‍♂️ Legjobb szett volumene sessionenként")

    exercise_list = workout_df['exercise_title'].unique()
    selected_exercise = st.selectbox("Válassz gyakorlatot a best set volumenhez:", exercise_list, key="best_set_exercise")

    period_option = st.radio("Időszak:", ["Elmúlt 3 hónap", "Elmúlt 1 év", "Minden idő"], key="best_set_period")
    now = pd.Timestamp.now()

    if period_option == "Elmúlt 3 hónap":
        cutoff = now - pd.DateOffset(months=3)
    elif period_option == "Elmúlt 1 év":
        cutoff = now - pd.DateOffset(years=1)
    else:
        cutoff = pd.Timestamp.min

    # Warmup szettek kizárása
    df = workout_df[
        (workout_df['exercise_title'] == selected_exercise) &
        (workout_df['set_type'] != 'warmup') &
        (workout_df['start_time'] >= cutoff)
    ].copy()

    if df.empty:
        st.warning("Nincs adat a kiválasztott gyakorlatra ebben az időszakban.")
        return

    df['session_id'] = df['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # Legjobb szett sessionenként
    best_set_volume = df.groupby('session_id').apply(lambda x: (x['weight_kg'] * x['reps']).max())
    best_set_volume = best_set_volume.sort_index()

    # Diagram
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(best_set_volume.index, best_set_volume.values, color='orange', edgecolor='black')

    # Oszlopok tetejére szöveg
    for bar, value in zip(bars, best_set_volume.values):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.5, f"{value:.0f}", ha='center', va='bottom', fontsize=9)

    ax.set_xlabel("Edzés dátuma")
    ax.set_ylabel("Best set volumen (kg×reps)")
    ax.set_title(f"{selected_exercise} – Legjobb szett volumene")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)


def session_volume_analysis(workout_df):
    st.subheader("📊 Gyakorlat Session Volumen Statisztika")

    exercise_list = workout_df['exercise_title'].unique()
    selected_exercise = st.selectbox("Válassz gyakorlatot:", exercise_list)

    period_option = st.radio("Időszak:", ["Elmúlt 3 hónap", "Elmúlt 1 év", "Minden idő"])
    now = pd.Timestamp.now()

    if period_option == "Elmúlt 3 hónap":
        cutoff = now - pd.DateOffset(months=3)
    elif period_option == "Elmúlt 1 év":
        cutoff = now - pd.DateOffset(years=1)
    else:
        cutoff = pd.Timestamp.min

    # Warmup szettek kizárása, minden más bele számít
    df = workout_df[
        (workout_df['exercise_title'] == selected_exercise) &
        (workout_df['set_type'] != 'warmup') &
        (workout_df['start_time'] >= cutoff)
    ].copy()

    if df.empty:
        st.warning("Nincs adat a kiválasztott gyakorlatra ebben az időszakban.")
        return

    df['session_id'] = df['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    session_volume = df.groupby('session_id').apply(lambda x: (x['weight_kg'] * x['reps']).sum())
    session_volume = session_volume.sort_index()

    # Diagram
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(session_volume.index, session_volume.values, color='skyblue', edgecolor='black')

    # Oszlopok tetejére szöveg
    for bar, value in zip(bars, session_volume.values):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.5, f"{value:.0f}", ha='center', va='bottom', fontsize=9)

    ax.set_xlabel("Edzés dátuma")
    ax.set_ylabel("Session volumen (kg×reps)")
    ax.set_title(f"{selected_exercise} – Session volumen")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)


def best_week_streak(df: pd.DataFrame, min_days_per_week=4) -> int:
    """
    Visszaadja a legjobb heti streaket, ahol legalább `min_days_per_week` edzés volt egy héten.
    """
    df = df.copy()
    df['date'] = df['start_time'].dt.date
    df['week'] = df['start_time'].dt.isocalendar().week
    df['year'] = df['start_time'].dt.isocalendar().year

    weekly_counts = df.groupby(['year', 'week'])['date'].nunique()
    streak_weeks = (weekly_counts >= min_days_per_week).astype(int)
    # Legnagyobb összefüggő streak
    max_streak = 0
    current = 0
    for val in streak_weeks:
        if val == 1:
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0
    return max_streak
