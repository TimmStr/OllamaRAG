# https://github.com/jborean93/smbprotocol/blob/master/examples/high-level/file-management.py


from os import mkdir

from smbclient import register_session, open_file, mkdir

from utils import load_smb_config, SMB_SERVER_HOST, SMB_SERVER_USER, SMB_SERVER_PASSWORD
from utils.logging_config import exception_handling


class SmbService:
    def __init__(self):
        config_dict = load_smb_config()
        ip = config_dict[SMB_SERVER_HOST]
        user = config_dict[SMB_SERVER_USER]
        password = config_dict[SMB_SERVER_PASSWORD]
        register_session(ip, username=user, password=password)

    def mk_dir(self, remote_folder_path):
        try:
            mkdir(remote_folder_path)
        except Exception as e:
            pass

    def read_from_server(self, remote_file_path):
        with open_file(remote_file_path, mode="rb") as file:
            content = file.read()
        return content

    @exception_handling
    def file_to_server(self, local_file_path, remote_file_path):
        with open_file(remote_file_path, mode="wb") as fd:
            with open(local_file_path, mode="rb") as file:
                content = file.read()
            fd.write(content)
