import csv
from django.core.management import BaseCommand, CommandError
from demo.models import Practice


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, path, **kwargs):
        release_date = path.split("-")[1].split(".")[0]
        if Practice.objects.filter(release_date=release_date).exists():
            raise CommandError(f"Already imported practices for {release_date}")

        with open(path) as f:
            for row in csv.DictReader(f):
                row["release_date"] = release_date
                Practice.objects.create(**row)
