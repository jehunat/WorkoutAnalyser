import pandas as pd
import matplotlib.pyplot as plt


def weekly_monthly_workout_trend(df: pd.DataFrame, freq: str = 'W'):
    """
    Heti / havi edzésszám trend grafikon.
    freq: 'W' = heti, 'M' = havi
    """
    df = df.copy()
    df['date'] = df['start_time'].dt.date

    trend_series = df.groupby(pd.Grouper(key='start_time', freq=freq)).size()

    fig, ax = plt.subplots(figsize=(8, 4))
    trend_series.plot(ax=ax, marker='o', linewidth=2)
    ax.set_title("Heti / havi edzésszám trend")
    ax.set_xlabel("Dátum")
    ax.set_ylabel("Edzésszám")
    plt.tight_layout()
    return fig


def exercise_weight_trend(df: pd.DataFrame, exercise_name: str):
    """
    Egy kiválasztott gyakorlat súlytrendje az időben (átlag súly edzésenként).
    """
    df_ex = df[df['exercise_title'] == exercise_name].copy()
    if df_ex.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Nincs adat ehhez a gyakorlathoz", ha='center', va='center')
        return fig

    df_ex['date'] = df_ex['start_time'].dt.date
    daily_avg = df_ex.groupby('date')['weight_kg'].mean()

    fig, ax = plt.subplots(figsize=(8, 4))
    daily_avg.plot(ax=ax, marker='o', color='orange')
    ax.set_title(f"{exercise_name} – átlag súly trend")
    ax.set_xlabel("Dátum")
    ax.set_ylabel("Átlag súly (kg)")
    plt.tight_layout()
    return fig


def exercise_progress(df: pd.DataFrame, exercise_name: str):
    """
    Ismétlés + súly fejlődés scatter grafikon gyakorlatonként.
    """
    df_ex = df[df['exercise_title'] == exercise_name].copy()
    if df_ex.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Nincs adat a kiválasztott gyakorlatról", ha='center', va='center')
        return fig

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df_ex['weight_kg'], df_ex['reps'], color='green', alpha=0.6)
    ax.set_title(f"{exercise_name} – súly / ismétlés fejlődés")
    ax.set_xlabel("Súly (kg)")
    ax.set_ylabel("Ismétlések száma")
    plt.tight_layout()
    return fig
