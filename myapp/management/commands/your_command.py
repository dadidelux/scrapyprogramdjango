from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of your command'

    def add_arguments(self, parser):
        # Optionally, you can add arguments to your command here
        pass

    def handle(self, *args, **kwargs):
        # The actual logic of your command
        self.stdout.write('Command executed successfully')
