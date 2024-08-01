"""Получение аргументов приложения, переданных в командной строке."""

import argparse
from app import data_attribute


class ArgumentParser:
    """Получение аргументов запуска приложения

    Raises:
        ValueError: исключение, возвращаемое в случае некорректного указания
        значения параметра
    """

    description = 'FTP/SFTP Synchronization'

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            description=ArgumentParser.description)
        self._get_arguments()
        self._args = self._parser.parse_args()
        if self._args.action not in data_attribute.Action.get_actions():
            raise ValueError(f'Неподдерживаемое действие {self._args.action}')

    def _get_arguments(self) -> None:
        self._parser.add_argument(
            '-a',
            '--action',
            type=str,
            help='Action (export/import)',
            required=True,
            choices=data_attribute.Action.get_actions()
        )
        self._parser.add_argument(
            '-c',
            '--config',
            type=str,
            required=False,
            default='config/config.ini',
            help='Custom config file path'
        )

    @property
    def action(self) -> str:
        """Возвращает переданное действие

        Returns:
            str: название действия (export/import)
        """
        return self._args.action
    
    @property
    def config(self) -> str:
        """Возвращает путь к файлу конфигурации, переданный приложению

        Returns:
            str: путь к файлу конфигурации клиента
        """
        return self._args.config