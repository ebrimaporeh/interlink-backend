# seeder/management/commands/seed_all.py
from django.core.management.base import BaseCommand
from seeder.seed_all import SeedAll

class Command(BaseCommand):
    help = 'Seed all database tables'
    
    def handle(self, *args, **options):
        self.stdout.write("Seeding entire database...")
        SeedAll.run()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))