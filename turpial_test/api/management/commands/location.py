import json
from django.core.management.base import BaseCommand, CommandError
from turpial_test.settings import BASE_DIR, FIXTURE_ROUTE
from api.serializers import RegionSerializer


class Command(BaseCommand):
    help = 'Load location data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start load locations'))
        with open(FIXTURE_ROUTE+'/locations.json', 'r') as f:
            data = json.load(f)
            data = data.get('data')
            import pudb;pudb.set_trace()
            serializer = RegionSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                print(str(serializer.errors))
