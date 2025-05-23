from os import environ
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

def enviar_correo(destinatarios: list[str], titulo: str, cuerpo: str):
    destinatarios = '.'.join(destinatarios)
    emailEmisor = environ.get('EMAIL_EMISOR')
    passwordEmisor = environ.get('PASSWORD_EMISOR')
    correo = MIMEMultipart()

    correo['Subject'] = titulo
    correo['From'] = emailEmisor
    correo['To'] = destinatarios

    texto = MIMEText(cuerpo,'plain')

    correo.attach(texto)

    servidorCorreo = SMTP('smtp.gmail.com') #gmail
    #servidorCorreo = SMTP('smtp.live.com') #hotmail
    servidorCorreo.starttls()

    servidorCorreo.login(emailEmisor, passwordEmisor)
    servidorCorreo.sendmail(from_addr=emailEmisor,
                            to_addrs=destinatarios, msg=correo.as_string())
    
    servidorCorreo.quit()

