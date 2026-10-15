import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ===== SQL Server =====
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_INSTANCE = os.getenv("DB_INSTANCE", "")  # optionnel

    # ===== SMTP =====
    SMTP_HOST = os.getenv("SMTP_HOST", "mail.cimsante.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    # ===== Email =====
    MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER)
    MAIL_RECIPIENTS = [e.strip() for e in os.getenv("MAIL_RECIPIENTS", "").split(",") if e.strip()]
    MAIL_CC = [e.strip() for e in os.getenv("MAIL_CC", "").split(",") if e.strip()]
    MAIL_SUBJECT = os.getenv("MAIL_SUBJECT", "Rapport journalier - {date}")

    @classmethod
    def get_db_url(cls):
        """Construit l'URL SQLAlchemy pour SQL Server via pyodbc."""
        # Si instance nommée : SERVER=host\instance
        server = f"{cls.DB_HOST}\\{cls.DB_INSTANCE}" if cls.DB_INSTANCE else cls.DB_HOST

        odbc_str = (
            f"DRIVER={{{cls.DB_DRIVER}}};"
            f"SERVER={server};"
            f"DATABASE={cls.DB_NAME};"
            f"UID={cls.DB_USER};"
            f"PWD={cls.DB_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )
        params = quote_plus(odbc_str)
        return f"mssql+pyodbc:///?odbc_connect={params}"