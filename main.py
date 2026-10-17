import logging
import os
from db import fetch_data
from excel_generator import generate_excel
from mail_sender import send_mail_with_attachment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("service.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 👉 Requête SQL Server (syntaxe T-SQL)
SQL_QUERY = """
    
"""


def run_job():
    logging.info("🚀 Démarrage du job journalier")
    try:
        logging.info("📊 Exécution de la requête SQL Server...")
        df = fetch_data(SQL_QUERY)
        logging.info(f"   → {len(df)} lignes récupérées")

        if df.empty:
            logging.warning("⚠️ Aucune donnée trouvée, arrêt du job")
            return

        logging.info("📝 Génération du fichier Excel...")
        filepath = generate_excel(df)

        logging.info("📧 Envoi de l'email via mail.cimsante.com...")
        send_mail_with_attachment(filepath, df_rows=len(df))

        os.remove(filepath)
        logging.info("✅ Job terminé avec succès")

    except Exception as e:
        logging.exception(f"❌ Erreur lors du job : {e}")


if __name__ == "__main__":
    run_job()
