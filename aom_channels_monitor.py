import epics
import time
import smtplib
from email.message import EmailMessage

EMAILS_TO_SEND = ['brojas@gemini.edu']


def on_conn_change(pvname=None, conn=None, **kws):
    """
    Function that detect and it's triggered when the PV state connection change
    :param pvname: the name of the PV
    :type pvname: str
    :param conn: the connection status
    :type conn: bool
    :param kws: additional keyword/value arguments
    :type kws: str
    """
    print(kws)

    if not conn:
        email_content = 'PV state connection change!', pvname, 'connected:', conn
        print(email_content)
        send_email(email_content)


def send_email(content):
    """
    Function that send the email of the channel disconnection to a specifics persons.
    :param content: The content of the message
    :type content: tuple
    """
    for email in EMAILS_TO_SEND:
        print('Email send to ' + email)
        msg = EmailMessage()
        msg['Subject'] = 'Timeout detected on channels'
        msg['From'] = 'brojas@gemini.edu'
        msg['To'] = email
        message = content
        msg.set_content(message)
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()


if __name__ == '__main__':

    # don't forget execute the following command line to have access to aom:health channel:
    # export EPICS_CA_ADDR_LIST=172.17.65.100

    # set up the PV
    p = epics.PV('aom:health', connection_callback=on_conn_change)
    # print('First value:', p.get())

    p.get()

    while True:
        epics.poll(evt=1.e-5, iot=0.1)
