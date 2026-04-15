import os
import resend


def send_mail(to: str, subject: str, html_body: str) -> None:
    resend.api_key = os.getenv("RESEND_API_KEY")

    if not resend.api_key:
        raise ValueError("RESEND_API_KEY tanımlı değil.")

    resend.Emails.send({
        "from": "Sabah Briefing <onboarding@resend.dev>",
        "to": [to],
        "subject": subject,
        "html": html_body,
    })
