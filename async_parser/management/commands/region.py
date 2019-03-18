from django.core.management.base import BaseCommand
from async_parser.tasks import create_table


class Command(BaseCommand):

    def handle(self, *args, **options):
        if options['number']:
            create_table(int(options['number']))

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            '-n',
            action='store',
            help='Number of region'
        )
