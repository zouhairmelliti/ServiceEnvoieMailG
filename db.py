import pandas as pd
from sqlalchemy import create_engine
from config import Config

def fetch_data(query: str, params: dict | None = None) -> pd.DataFrame:
    """Exécute une requête SQL Server et retourne un DataFrame."""
    engine = create_engine(
        Config.get_db_url(),
        fast_executemany=True,   # performance pyodbc
        pool_pre_ping=True       # vérifie la connexion avant usage
    )
    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        engine.dispose()