import epics
import time
import smtplib
from email.message import EmailMessage

EMAILS_TO_SEND = ['brojas@gemini.edu']
CHANNELS_LIST = ['aom:health']
# CHANNELS_LIST = ['ws:present', 'ec:present']


def on_conn_change(pvname=None, conn=None, **kws):
    """
    Function that detect and it's triggered when the PV connection status changed.
    :param pvname: the name of the PV
    :type pvname: str
    :param conn: the connection status
    :type conn: bool
    :param kws: additional keyword/value arguments
    :type kws: str
    """

    if not conn:
        email_content = "\n" + 'Channel ' + pvname + ' connection status changed! to disconnected.'
        send_email(email_content, pvname)
        print(email_content)
    else:
        print(kws)
        print(pvname)
        print(conn)


def send_email(content, header):
    """
    Function that send the email of the channel disconnection to a specifics persons.
    :param header: The channel name
    :type header: str
    :param content: The content of the message
    :type content: str
    """
    for email in EMAILS_TO_SEND:
        print('Email send to ' + email)
        msg = EmailMessage()
        msg['Subject'] = 'Timeout connection detected on ' + header
        msg['From'] = 'brojas@gemini.edu'
        msg['To'] = email
        note = '\n' + '\n' + 'NOTE: Please check the AOM channels.'
        message = content + note
        msg.set_content(message)
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()


if __name__ == '__main__':

    # don't forget execute the following command line to have access to aom:health channel:
    # export EPICS_CA_ADDR_LIST=172.17.65.100

    # set up the PV
    for name in CHANNELS_LIST:
        p = epics.PV(name, connection_callback=on_conn_change)

    while True:
        epics.poll(evt=1.e-5, iot=0.1)
