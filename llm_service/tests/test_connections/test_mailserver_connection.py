import pytest
from unittest import mock
from utils import MAIL_HOST, MAIL_PORT, MAIL_USER, MAIL_PASSWORD
from connections.mailserver_connection import EmailService


@pytest.fixture
def mock_email_service():
    with mock.patch('smtplib.SMTP') as mock_smtp:
        mock_mail_config = {
            MAIL_HOST: 'smtp.xyz.com',
            MAIL_PORT: 587,
            MAIL_USER: 'user',
            MAIL_PASSWORD: 'password',
            "email_from": 'from@example.com'
        }
        print(mock_mail_config[MAIL_PORT])
        with mock.patch('utils.mail_config', return_value=mock_mail_config):
            service = EmailService()
            yield service
            mock_smtp.assert_called_once_with(mock_mail_config[MAIL_HOST], int(mock_mail_config[MAIL_PORT]))


def test_send_mail(mock_email_service):
    with mock.patch.object(mock_email_service.mailserver_conn, 'sendmail') as mock_sendmail:
        mock_email_service.send_mail("Test Subject", "Test Text", "test@xyz.de")
        mock_sendmail.assert_called_once()

        args, kwargs = mock_sendmail.call_args
        assert args[0] == "from@example.com"
        assert args[1] == "test@xyz.de"
        assert 'Test Subject' in args[2]
        assert 'Test Text' in args[2]


def test_send_mail_invalid_address(mock_email_service):
    with mock.patch.object(mock_email_service.mailserver_conn, 'sendmail') as mock_sendmail, \
            mock.patch('builtins.print') as mock_print:
        mock_email_service.send_mail("Test Subject", "Test Text", "invalid@xyz.org")
        mock_sendmail.assert_not_called()
        mock_print.assert_called_once_with("wrong email")


def test_send_mail_exception_handling(mock_email_service):
    error_msg = "SMTP Error"
    with mock.patch.object(mock_email_service.mailserver_conn, 'sendmail', side_effect=Exception(error_msg)):
        with pytest.raises(Exception, match=error_msg):
            mock_email_service.send_mail("Test Subject", "Test Text", "test@xyz.de")


def test_email_service_cleanup(mock_email_service):
    with mock.patch.object(mock_email_service.mailserver_conn, 'quit') as mock_quit:
        del mock_email_service
        mock_quit.assert_called_once()
