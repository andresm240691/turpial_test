import json
from django.core.management.base import BaseCommand, CommandError
from turpial_test.settings import BASE_DIR, FIXTURE_ROUTE
from api.serializers import PokemonSerializer


class Command(BaseCommand):
    help = 'Load pokemon data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start load pokemons'))
        with open(FIXTURE_ROUTE+'/pokemons.json', 'r') as f:
            data = json.load(f)
            pokemon_list = data.get('data')
            pokemon_serialzier = PokemonSerializer(data=pokemon_list, many=True)
            if pokemon_serialzier.is_valid():
                pokemon_serialzier.save()
            else:
                print(str(pokemon_serialzier.errors))
        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))