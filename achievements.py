import pandas as pd


def best_week_streak(df, min_days_per_week=4):
    """
    Maximum egymást követő heti streak, amikor legalább `min_days_per_week` különböző napra esett edzés történt.
    """
    if df.empty:
        return 0

    df = df.copy()
    df['date'] = df['start_time'].dt.normalize()
    df['week_start'] = df['date'] - pd.to_timedelta(df['date'].dt.weekday, unit='d')  # hét kezdete (hétfő)

    # Egyedi napok száma hétre lebontva
    weekly_unique_days = df.groupby('week_start')['date'].nunique().reset_index(name='unique_days')
    weekly_unique_days['meets_goal'] = weekly_unique_days['unique_days'] >= min_days_per_week

    # Rendezés dátum szerint
    weekly_unique_days = weekly_unique_days.sort_values('week_start')

    # Streak számítás
    max_streak = 0
    current_streak = 0
    last_week = None
    for _, row in weekly_unique_days.iterrows():
        if row['meets_goal']:
            if last_week is None or (row['week_start'] - last_week).days == 7:
                current_streak += 1
            else:
                current_streak = 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
        last_week = row['week_start']

    return max_streak


def get_achievements(workout_df: pd.DataFrame):
    """
    Visszaadja a felhasználó badge-jeit az edzésadatok alapján.
    """

    badges = []

    if workout_df.empty:
        return badges

    # --- 1. Edzés streak ---
    workout_df = workout_df.sort_values("start_time")
    unique_days = sorted(workout_df["start_time"].dt.normalize().unique())

    streak = 1
    max_streak = 1
    for i in range(1, len(unique_days)):
        if (unique_days[i] - unique_days[i - 1]).days == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    # Streak badge-ek
    if max_streak >= 3:
        badges.append("🟢 3 napos streak – Kezdő lendület")
    if max_streak >= 7:
        badges.append("🔵 7 napos streak – Heti warrior")
    if max_streak >= 30:
        badges.append("🟣 30 napos streak – Egy hónap a kitartásért")
    if max_streak >= 90:
        badges.append("🏅 90 napos streak – Legendás edző")

    # --- 2. Súly / PR badge-ek ---
    # Minden gyakorlatra nézzük a max súlyt
    exercises = workout_df['exercise_title'].unique()
    for ex in exercises:
        ex_df = workout_df[(workout_df['exercise_title'] == ex) & (workout_df['set_type'] == 'normal')]
        if not ex_df.empty:
            max_weight = ex_df['weight_kg'].max()
            if max_weight >= 100:
                badges.append(f"🏋️ {ex} PR {int(max_weight)} kg")

    # --- 3. Heti aktivitás badge-ek ---
    # Aktuális hét napjai
    current_week = pd.Timestamp.now().isocalendar().week
    df_current_week = workout_df[workout_df['start_time'].dt.isocalendar().week == current_week]
    weekly_sessions = df_current_week['start_time'].dt.date.nunique()

    if weekly_sessions >= 3:
        badges.append("📅 Heti 3 edzés – Következetes")
    if weekly_sessions >= 5:
        badges.append("💪 Heti 5 edzés – Pro edző")

    # --- 4. Sokoldalúság / variáció ---
    unique_exercises_count = workout_df['exercise_title'].nunique()
    if unique_exercises_count >= 5:
        badges.append("🎯 5+ különböző gyakorlat – Sokoldalú")
    if unique_exercises_count >= 10:
        badges.append("⚡ 10+ különböző gyakorlat – Teljes test mester")

    # --- 5. Hosszútávú achievement ---
    years_tracked = workout_df['start_time'].dt.year.nunique()
    if years_tracked >= 1:
        badges.append("🏆 1 év edzés – Éves hős")
    if years_tracked >= 2:
        badges.append("🥇 2+ év edzés – Veterán edző")

    return badges

