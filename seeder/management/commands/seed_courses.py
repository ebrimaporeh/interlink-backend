# seeder/management/commands/seed_courses.py
from django.core.management.base import BaseCommand
from seeder.seed_courses import SeedCourses

class Command(BaseCommand):
    help = 'Seed courses data'
    
    def handle(self, *args, **options):
        self.stdout.write("Seeding courses...")
        SeedCourses.run()
        self.stdout.write(self.style.SUCCESS("Courses seeded successfully!"))