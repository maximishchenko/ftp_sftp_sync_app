import enum
from dataclasses import dataclass

class Config(enum.Enum):

    default_config = 'config/config.ini'

    remote_host_section = 'RemoteHost'
    remote_host_protocol = 'protocol'
    remote_host_address = 'address'
    remote_host_port = 'port'
    remote_host_username = 'username'
    remote_host_password = 'password'

    remote_fs_section ='RemoteFS'
    remote_fs_export = 'export_dir'
    remote_fs_import = 'import_dir'

    local_fs_section = 'LocalFS'
    local_fs_export = 'export_dir'
    local_fs_import = 'import_dir'


class Protocol(enum.Enum):
    FTP = 'ftp'
    SFTP ='sftp'

    @staticmethod
    def get_protocols() -> tuple:
        return (Protocol.FTP.value, Protocol.SFTP.value)
    

class Action(enum.Enum):
    EXPORT = 'export'
    IMPORT = 'import'


    @staticmethod
    def get_actions() -> tuple:
        return (Action.EXPORT.value, Action.IMPORT.value)
    

@dataclass
class RemoteHostConfig:
    protocol: str
    address: str
    port: int
    username: str
    password: str


@dataclass
class RemoteFsConfig:
    export_dir: str
    import_dir: str


@dataclass
class LocalFsConfig:
    export_dir: str
    import_dir: str