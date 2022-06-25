import json
from django.core.management.base import BaseCommand, CommandError
from turpial_test.settings import BASE_DIR, FIXTURE_ROUTE
from api.serializers import AreaSerializer


class Command(BaseCommand):
    help = 'Load area data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start load areas'))
        with open(FIXTURE_ROUTE+'/areas.json', 'r') as f:
            data = json.load(f)
            areas_data = data.get('data')
            ad = AreaSerializer(data=areas_data, many=True)
            if ad.is_valid():
                ad.save()
            else:
                print(str(ad.errors))
