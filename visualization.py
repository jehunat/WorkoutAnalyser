import matplotlib.pyplot as plt
import pandas as pd


def plot_top_exercises(top_df: pd.DataFrame):
    """Top gyakorlatok oszlopdiagramja dinamikusan méretezve."""
    top_n = len(top_df)
    fig_width = max(7, 0.5 * top_n + 6)
    fig_height = 4
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    ax.bar(top_df['exercise_title'], top_df['sessions_count'], color='skyblue', edgecolor='black')
    ax.set_xlabel("Gyakorlat")
    ax.set_ylabel("Edzésnapok száma")
    ax.set_title(f"Top {top_n} gyakorlat")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def multi_year_workout_heatmap(workout_df: pd.DataFrame):
    """GitHub-stílusú éves heatmap."""
    df = workout_df.copy().dropna(subset=['start_time'])
    df['date'] = df['start_time'].dt.normalize()
    df['year'] = df['date'].dt.year
    years = sorted(df['year'].unique())

    figs = []
    for year in years:
        df_year = df[df['year'] == year]
        total_workouts = df_year['date'].nunique()
        all_days = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31')
        activity = pd.DataFrame({'date': all_days})
        daily_counts = df_year.groupby('date').size().reset_index(name='workout_count')
        activity = activity.merge(daily_counts, on='date', how='left').fillna(0)
        activity['week'] = activity['date'].dt.isocalendar().week
        activity['weekday'] = activity['date'].dt.weekday
        pivot = activity.pivot_table(index='weekday', columns='week', values='workout_count', aggfunc='sum',
                                     fill_value=0)

        fig, ax = plt.subplots(figsize=(15, 2))
        im = ax.imshow(pivot, cmap='Greens', aspect='auto', interpolation='nearest')
        ax.set_yticks(range(7))
        ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        ax.set_title(f"{year} – {total_workouts} workout day(s)")
        ax.set_xlabel("Week of Year")
        figs.append(fig)
    return figs


def plot_goal_progress_sets(best_sets_df, exercise_title, target_weight=None):
    """
    Legjobb working szettek grafikon:
    - X: szettek sorszáma 1..N
    - Y: ismétlés
    - Célsúly a címben
    """
    if best_sets_df.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Nincs adat a kiválasztott gyakorlatból", ha='center', va='center')
        return fig

    fig, ax = plt.subplots(figsize=(8, 4))

    # X tengely: szettek 1..N
    x = list(range(1, len(best_sets_df) + 1))
    y = best_sets_df['reps'].tolist()
    ax.bar(x, y, color='skyblue', edgecolor='black')

    for xi, rep in zip(x, y):
        ax.text(xi, rep + 0.2, str(rep), ha='center', va='bottom', fontsize=10)

    ax.set_xlabel("Szettek")
    ax.set_ylabel("Ismétlés")

    last_date = best_sets_df['start_time'].max().date() if 'start_time' in best_sets_df.columns else ""
    if target_weight:
        plt.title(f"{exercise_title} – {target_weight} kg, legjobb szettek ({last_date})")
    else:
        plt.title(f"{exercise_title} – legjobb szettek ({last_date})")

    plt.ylim(0, max(best_sets_df['reps'].max(), 10) + 2)
    plt.xticks(x)  # X-tengelyen 1,2,3...
    plt.tight_layout()
    return fig


