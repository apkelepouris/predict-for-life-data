"""
Predict For Life - Email Notifier

Sends email notifications for important
automation events.
"""

from __future__ import annotations

import os
import smtplib

from email.message import EmailMessage


class EmailNotifier:
    """
    Sends automation email notifications.
    """

    def send(
        self,
        subject: str,
        body: str,
    ) -> None:
        """
        Send an email notification.
        """

        smtp_server = os.environ["SMTP_SERVER"]
        smtp_port = int(
            os.environ["SMTP_PORT"]
        )
        username = os.environ["SMTP_USERNAME"]
        password = os.environ["SMTP_PASSWORD"]
        recipient = os.environ[
            "NOTIFICATION_EMAIL"
        ]

        message = EmailMessage()

        message["Subject"] = subject
        message["From"] = username
        message["To"] = recipient

        message.set_content(body)

        with smtplib.SMTP(
            smtp_server,
            smtp_port,
        ) as smtp:

            smtp.starttls()

            smtp.login(
                username,
                password,
            )

            smtp.send_message(
                message,
            )