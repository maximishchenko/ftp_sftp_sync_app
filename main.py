from app.argument import ArgumentParser
from app.config import ConfigurationParser
from app.data_attribute import (
    RemoteHostConfig,
    RemoteFsConfig,
    LocalFsConfig,
    Action
)
from app.sync import RemoteFsClientFactory, LocalFs
import os
import logging

logger = logging.getLogger(__name__)


def main():
    args = ArgumentParser()
    config = ConfigurationParser()
    host_config = RemoteHostConfig(**config.get_remote_host_params())
    remote_fs_config = RemoteFsConfig(**config.get_remote_fs_params())
    local_fs_config = LocalFsConfig(**config.get_local_fs_params())
    

    remote_fs_client = RemoteFsClientFactory(host_config=host_config)
    if args.action == Action.EXPORT.value:
        files_to_export = LocalFs.get_files(local_fs_config.export_dir)
        for local_file in files_to_export:
            file_name = os.path.basename(local_file)
            remote_file = f"{remote_fs_config.import_dir}/{file_name}"
            remote_fs_client.export_file(local_file, remote_file)
    elif args.action == Action.IMPORT.value:
        remote_fs = remote_fs_client.list_dir(remote_fs_config.export_dir)
        for remote_file in remote_fs:
            local_file = f"{local_fs_config.import_dir}\\{remote_file}"
            remote_fs_client.import_file(remote_file, local_file)
    else:
        logger.warning(f"Действие неизвестно: {args.action}")
    remote_fs_client.disconnect()


if __name__ == '__main__':
    main()  
