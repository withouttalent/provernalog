from django.core.management.base import BaseCommand, CommandError
from async_parser.tasks import fetch_rosreestr, Parcel
from django.conf import settings
from numpy import array_split
class Command(BaseCommand):


    def handle(self, *args, **options):
        region = options['region']
        parcels = Parcel.objects.filter(region=int(region)).values('cadastral_number')
        parcels = list(parcels)
        parcels = array_split(parcels, 64)
        for parcel in parcels:
            if settings.DEBUG:
                fetch_rosreestr(list(parcel))
            else:
                fetch_rosreestr(list(parcel))


    def add_arguments(self, parser):
        parser.add_argument(
            '--group_type',
            '-gt',
            action="store",
            default=None,
            help="Парсинг кадастровых объектов"
        )
        parser.add_argument(
            '--region',
            action='store',
            help="Create partition with new region"
        )
