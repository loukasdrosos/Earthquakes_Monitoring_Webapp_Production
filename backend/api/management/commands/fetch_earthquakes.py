from django.core.management.base import BaseCommand

from api.services import fetch_and_save_earthquakes_from_xml


class Command(BaseCommand):
    help = "Fetch and parse earthquake data from XML feed"

    def handle(self, *args, **kwargs):
        result = fetch_and_save_earthquakes_from_xml()

        self.stdout.write(
            self.style.SUCCESS(
                f"Fetch complete. Created: {result['created']}, Existing: {result['existing']}, Errors: {len(result['errors'])}"
            )
        )

        for error in result["errors"][:20]:
            self.stderr.write(error)