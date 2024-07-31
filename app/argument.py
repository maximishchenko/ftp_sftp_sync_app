import argparse
from app import data_attribute


class ArgumentParser:

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
    def action(self):
        return self._args.action
    
    @property
    def config(self):
        return self._args.config