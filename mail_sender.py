import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr, formatdate, make_msgid
from datetime import datetime
from config import Config


def send_mail_with_attachment(filepath: str, df_rows: int = 0) -> None:
    """Envoie l'email avec le fichier Excel en pièce jointe via mail.cimsante.com."""
    date_str = datetime.now().strftime("%d/%m/%Y")

    body_text = (
        f"Bonjour,\n\n"
        f"Veuillez trouver ci-joint le rapport journalier des examens radiologiques du {date_str}, "
        f"généré automatiquement le {date_str}.\n\n"
        f"Ce fichier contient {df_rows} enregistrement(s) extrait(s) de la base "
        f"de données pour la journée écoulée.\n\n"
        f"Cordialement,\n"
        f"Le service automatique de reporting CRIT"
    )

    msg = MIMEMultipart()
    msg["From"] = formataddr(("Reporting CRIT", Config.MAIL_FROM))
    msg["To"] = ", ".join(Config.MAIL_RECIPIENTS)
    if Config.MAIL_CC:
        msg["CC"] = ", ".join(Config.MAIL_CC)
    msg["Subject"] = Config.MAIL_SUBJECT.format(date=date_str)
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="cimsante.com")

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    filename = filepath.split("/")[-1].split("\\")[-1]
    with open(filepath, "rb") as f:
        part = MIMEApplication(
            f.read(),
            _subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    part["Content-Disposition"] = f'attachment; filename="{filename}"'
    msg.attach(part)

    # ===== Connexion SMTP selon le port =====
    if Config.SMTP_PORT == 465:
        # SSL implicite
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT, context=context) as server:
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)
    else:
        # STARTTLS (587) ou sans chiffrement (25)
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT, timeout=30) as server:
            server.ehlo()
            if Config.SMTP_USE_TLS:
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.ehlo()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)

    all_recipients = Config.MAIL_RECIPIENTS + Config.MAIL_CC

    print(f"Email envoye a : {', '.join(all_recipients)}")