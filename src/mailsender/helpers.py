from django.template import Context
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time


def createMails(template, subject, contacts, sender):
    mails = []
    for contact in contacts:
        mail_subject = subject.render(Context(contact.contact_info))
        mail_content = template.render(Context(contact.contact_info))
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = contact.email
        msg["Subject"] = mail_subject
        msg.attach(MIMEText(mail_content, "html"))
        mails.append(msg)
    return mails


def connect_to_smtp_server(smtp_server="correo.ugr.es", smtp_port=587):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        while not test_conn_open(server):
            time.sleep(5)
        print("SMTP connection successful!")
        return server
    except Exception as e:
        print("An error occurred while connecting to the SMTP server:", str(e))
        return None


def test_conn_open(conn):
    try:
        status = conn.noop()[0]
    except:  # smtplib.SMTPServerDisconnected
        status = -1
    return True if status == 250 else False


def send_mass_html_mail(
    messages, sender_email, sender_user, sender_password, smtp_server, smtp_port
):
    """
    Given an array of messages, sends each message to each recipient list. Returns the
    number of emails sent.
    """
    try:
        server = None
        nb_of_tries = 3
        while server is None and nb_of_tries > 0:
            print("Retrying smtp connection...")
            server = connect_to_smtp_server(smtp_server, smtp_port)
            nb_of_tries = nb_of_tries - 1
        if server is None:
            raise Exception("Could not connect to server")

        server.starttls()
        server.ehlo_or_helo_if_needed()

        response = server.login(sender_user, sender_password)
        if response[0] == 235:
            print("Authorization successful")
        else:
            print("Authorization failed. Response:", response)

        result = []
        for msg in messages:
            try:
                res = server.sendmail(sender_email, msg["To"], msg.as_string())
                if len(res) > 0:
                    for recipient, error in result.items():
                        result.append(f"Recipient: {recipient}, Error: {error}")
            except Exception as e:
                result.append(e)

        return result

    except Exception as e:
        raise Exception(e)

    finally:
        try:
            server.quit()
        except Exception as e:
            raise Exception(e)
