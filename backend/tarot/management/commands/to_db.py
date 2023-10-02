from django.core.management.base import BaseCommand
from tarot.models import Card
import json
from django.core.files.base import ContentFile
from django.core.files import File


class Command(BaseCommand):
    help = 'JSON to db'

    def handle(self, *args, **options):
        with open('../tarot_db_en.json', 'r') as tarot_file:
            tarot_cards = json.load(tarot_file)

        for card, data in tarot_cards.items():
            card_to_db = Card(
                card=card,
                finance=data['finance'],
                love=data['love'],
                day=data['day'],
                advise=data['advise'],
                yes_or_no=data['yes_or_no'],
            )

            card_to_db.save()
            with open(f'../cards/{card}.png', "rb") as img:
                djangofile = File(img)
                card_to_db.image.save('{card}.png', djangofile)

