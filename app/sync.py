import abc
import ftplib
import os
import paramiko
from app.data_attribute import (RemoteHostConfig, Protocol)


class LocalFs:

    @staticmethod
    def get_files(path: str) -> tuple:
        return tuple([f"{path}\\{file}" for file in os.listdir(path)])
    

class RemoteFsClient(abc.ABC):

    @abc.abstractmethod
    def list_dir(self, remote_dir: str) -> list: pass

    @abc.abstractmethod
    def export_file(self, local_file: str, remote_file: str) -> None: pass

    @abc.abstractmethod
    def import_file(self, remote_file: str, local_file: str) -> None: pass

    def disconnect(self) -> None: pass


class SftpClient(RemoteFsClient):

    def __init__(self, host_config: RemoteHostConfig):
        transport = paramiko.Transport(
            host_config.address,
            host_config.port
        )
        transport.connect(
            username=host_config.username,
            password=host_config.password
        )
        self._client = paramiko.SFTPClient.from_transport(transport)

    def export_file(self, local_file: str, remote_file: str) -> None:
        if not self._client:
            raise RuntimeError("Параметры клиента не определены")
        self._client.put(local_file, remote_file)

    def import_file(self, remote_file: str, local_file: str) -> None:
        if not self._client:
            raise RuntimeError("Параметры клиента не определены")
        self._client.get(remote_file, local_file)

    def list_dir(self, remote_dir: str) -> list:
        if not self._client:
            raise RuntimeError("Параметры клиента не определены")
        return self._client.listdir(remote_dir)

    def disconnect(self) -> None:
        if not self._client:
            raise RuntimeError("Параметры клиента не определены")
        self._client.close()



class FtpClient(RemoteFsClient):

    def __init__(self, host_config: RemoteHostConfig):
        self._client = ftplib.FTP()
        self._client.connect(host=host_config.address, port=host_config.port)
        self._client.login(host_config.username, host_config.password)
        self._client.encoding = "utf-8"

    def list_dir(self, remote_dir: str) -> list:
        self._client.cwd(remote_dir)
        return self._client.nlst()

    def export_file(self, local_file: str, remote_file: str) -> None:
        with open(local_file, "rb") as file:
            self._client.storbinary(f"STOR {remote_file}", file)
    
    def import_file(self, remote_file: str, local_file: str) -> None:
        with open(local_file, 'wb') as file:
            self._client.retrbinary(f'RETR {remote_file}', file.write)
    
    def disconnect(self) -> None:
        self._client.quit()
    

class RemoteFsClientFactory:

    def __new__(cls, host_config):
        if host_config.protocol == Protocol.SFTP.value:
            return SftpClient(host_config=host_config)
        elif host_config.protocol == Protocol.FTP.value:
            return FtpClient(host_config=host_config)
        else:
            raise RuntimeError("Неподдерживаемый протокол")