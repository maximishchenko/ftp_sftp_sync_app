"""Обработка полученной конфигурации приложения"""
import configparser
from app.data_attribute import Config


class ConfigurationParser:
    """Обработка конфигурации приложения."""

    def __init__(self, config = Config.default_config.value):
        self._config = configparser.ConfigParser()
        self._config.read(config, encoding='utf-8')

    def get_remote_host_params(self) -> dict:
        return {
            Config.remote_host_protocol.value: self._config.get(
                Config.remote_host_section.value,
                Config.remote_host_protocol.value
            ),
            Config.remote_host_address.value: self._config.get(
                Config.remote_host_section.value,
                Config.remote_host_address.value
            ),
            Config.remote_host_port.value: self._config.getint(
                Config.remote_host_section.value,
                Config.remote_host_port.value
            ),
            Config.remote_host_username.value: self._config.get(
                Config.remote_host_section.value,
                Config.remote_host_username.value
            ),
            Config.remote_host_password.value: self._config.get(
                Config.remote_host_section.value,
                Config.remote_host_password.value
            )
        } 
    
    def get_remote_fs_params(self) -> dict:
        return {
            Config.remote_fs_export.value: self._config.get(
                Config.remote_fs_section.value,
                Config.remote_fs_export.value
            ),
            Config.remote_fs_import.value: self._config.get(
                Config.remote_fs_section.value,
                Config.remote_fs_import.value
            )
        }

    def get_local_fs_params(self) -> dict:
        return {
            Config.local_fs_export.value: self._config.get(
                Config.local_fs_section.value,
                Config.local_fs_export.value
            ),
            Config.local_fs_import.value: self._config.get(
                Config.local_fs_section.value,
                Config.local_fs_import.value
            )
        }