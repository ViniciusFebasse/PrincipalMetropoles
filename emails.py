import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from acessos import servidor, porta, usuario, senha, destinatarios


class EnviarEmail:
    def __init__(self, assunto, mensagem):
        # Configuração
        host = servidor
        port = porta
        user = usuario
        password = senha
        destinos = destinatarios

        # Criando objeto
        print('Criando objeto servidor...')
        server = smtplib.SMTP(host, port)

        # Login com servidor
        print('Login...')
        server.ehlo()
        server.starttls()
        server.login(user, password)

        # Criando mensagem
        message = mensagem

        print('Criando mensagem...')

        i = 1
        for emails in destinos:
            email_msg = MIMEMultipart()
            email_msg['From'] = user
            email_msg['To'] = emails
            email_msg['Subject'] = assunto
            print('Adicionando texto...')

            email_msg.attach(MIMEText(message, 'plain'))

            # Enviando mensagem
            print('Enviando mensagem...')
            server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
            print(f'Mensagem nº {i} enviada!')
            i += 1
        server.quit()