import pandas as pd

def load_workouts(filepath: str) -> pd.DataFrame:
    """Betölti az edzésadatokat és átalakítja a dátumokat datetime-re."""
    df = pd.read_csv(filepath)
    df['start_time'] = pd.to_datetime(df['start_time'], dayfirst=True, errors='coerce')
    df['end_time'] = pd.to_datetime(df['end_time'], dayfirst=True, errors='coerce')
    return df

def get_unique_sessions(df: pd.DataFrame) -> pd.DataFrame:
    """Visszaadja az egyedi edzéseket (minden edzés egyszer szerepeljen)."""
    unique_sessions = df[['title', 'start_time', 'end_time']].drop_duplicates()
    unique_sessions['duration'] = unique_sessions['end_time'] - unique_sessions['start_time']
    return unique_sessions
