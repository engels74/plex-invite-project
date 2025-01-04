import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from .config import SMTPConfig

class SMTPSender:
    """Handles sending emails through SMTP"""
    
    def __init__(self, config: SMTPConfig):
        self.config = config
        self._server: Optional[smtplib.SMTP] = None

    def connect(self) -> None:
        """Connect to SMTP server"""
        try:
            self._server = smtplib.SMTP(
                host=self.config.host,
                port=self.config.port,
                timeout=self.config.timeout
            )
            
            if self.config.use_tls:
                self._server.starttls()
            
            self._server.login(self.config.username, self.config.password)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SMTP server: {str(e)}")

    def test_connection(self) -> bool:
        """Test SMTP server connection"""
        try:
            self.connect()
            if self._server:
                self._server.quit()
            return True
        except smtplib.SMTPException:
            if self._server:
                try:
                    self._server.quit()
                except smtplib.SMTPException:
                    pass
            return False

    def send_email(self, to: str, subject: str, body: str) -> None:
        """Send an email"""
        if self._server is None:
            raise ConnectionError("Not connected to SMTP server")
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.from_email
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            self._server.sendmail(
                self.config.from_email,
                to,
                msg.as_string()
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}")

    def disconnect(self) -> None:
        """Disconnect from SMTP server"""
        if self._server:
            try:
                self._server.quit()
            except Exception:
                pass
            finally:
                self._server = None