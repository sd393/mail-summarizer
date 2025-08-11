import email_loader, email_sender, summarizer

text = email_loader.format_email_info()
email_sender.send_email(summarizer.get_summary(text))
