import os

from dotenv import load_dotenv

from utils.constants import MAIL_USER, MAIL_HOST, MAIL_PASSWORD, MAIL_PORT, SMB_SERVER_HOST, SMB_SERVER_PATH, \
    SMB_SERVER_USER, SMB_SERVER_PASSWORD
from utils.logging_config import exception_handling

load_dotenv()


def mail_config():
    return {
        MAIL_HOST: os.getenv(MAIL_HOST),
        MAIL_USER: os.getenv(MAIL_USER),
        MAIL_PASSWORD: os.getenv(MAIL_PASSWORD),
        MAIL_PORT: os.getenv(MAIL_PORT)
    }


def load_smb_config():
    return {
        SMB_SERVER_HOST: os.getenv(SMB_SERVER_HOST),
        SMB_SERVER_PATH: os.getenv(SMB_SERVER_PATH),
        SMB_SERVER_USER: os.getenv(SMB_SERVER_USER),
        SMB_SERVER_PASSWORD: os.getenv(SMB_SERVER_PASSWORD)
    }
