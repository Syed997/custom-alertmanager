import smtplib

with smtplib.SMTP("localhost", 1025) as server:
    server.sendmail("from@example.com", "to@example.com", "Test email via MailHog")
