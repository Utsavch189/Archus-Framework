import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl
import sys


TLS_PORT = 587  # Port for TLS
NON_TLS_PORT = 25  # Port for non-TLS
SSL_PORT = 465  # Port for SSL

class SendMail:
    def __init__(self,BASE_DIR=None,SMTP_SERVER:str="",SMTP_PASSWORD:str="",SMTP_USERNAME:str="",use_tls=True,use_ssl=False) -> None:
        if not BASE_DIR:
            raise Exception("Base directory must be specified")

        self.BASE_DIR=BASE_DIR
        sys.path.append(self.BASE_DIR)

        try:
            import config
        except Exception as e:
            pass
        
        self.SMTP_SERVER=SMTP_SERVER or config.SMTP_SERVER
        self.SMTP_PASSWORD=SMTP_PASSWORD or config.SMTP_PASSWORD
        self.SMTP_USERNAME=SMTP_USERNAME or config.SMTP_USERNAME
        self.use_tls=use_tls or config.SMTP_USE_TLS
        self.use_ssl=use_ssl or config.SMTP_USE_SSL

    def send_email(self,subject:str, body:str, to:str, html=False, attachment=None):
        message = MIMEMultipart()
        message["From"] = self.SMTP_USERNAME
        message["To"] = to
        message["Subject"] = subject

        if html:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))

        if attachment:
            try:
                with open(attachment, "rb") as attach_file:
                    attachment_part = MIMEBase("application", "octet-stream")
                    attachment_part.set_payload(attach_file.read())
                    encoders.encode_base64(attachment_part)
                    attachment_part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attachment)}"
                    )
                    message.attach(attachment_part)
            except Exception as e:
                print(f"Error attaching file: {e}")
        
        port = TLS_PORT if self.use_tls else NON_TLS_PORT
        if self.use_ssl:
            port = SSL_PORT
        
        try:
            if self.use_ssl:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(self.SMTP_SERVER, port, context=context)
            else:
                server = smtplib.SMTP(self.SMTP_SERVER, port)
                if self.use_tls:
                    server.starttls()
        except Exception as e:
            print(e)
        
        try:
            server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
            server.sendmail(self.SMTP_USERNAME, to, message.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()

if __name__=="__main__":
    html_content = """
    <html>
        <body>
            <h1 style="color:blue;">HTML Email Example</h1>
            <p>This is a <strong>styled</strong> HTML email body.</p>
        </body>
    </html>
    """
    mail=SendMail(
        'smtp.gmail.com',
        'nzlettvkyviafplp',
        'utsavpokemon9000chatterjee@gmail.com'
    )
    mail.send_email(
        subject="Test",
        to="utsavchatterjee71@gmail.com",
        body=html_content,
        html=True
    )