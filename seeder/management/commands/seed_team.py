# seeder/management/commands/seed_team.py
from django.core.management.base import BaseCommand
from seeder.seed_team import SeedTeam

class Command(BaseCommand):
    help = 'Seed team members data'
    
    def handle(self, *args, **options):
        self.stdout.write("Seeding team members...")
        SeedTeam.run()
        self.stdout.write(self.style.SUCCESS("Team members seeded successfully!"))