# seeder/seed_users.py
from django.contrib.auth.models import User
from accounts.models import UserProfile
from . import BaseSeeder

class SeedUsers(BaseSeeder):
    @staticmethod
    def run():
        print("\n👤 Seeding Users...")
        
        # Clear existing users (except superuser)
        User.objects.exclude(is_superuser=True).delete()
        
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@interlinkglobal.edu',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            BaseSeeder.print_success("Created admin user")
        
        # Create staff users
        staff_users = [
            {'username': 'momodou.darboe', 'email': 'momodou@interlinkglobal.edu', 'first_name': 'Momodou', 'last_name': 'Darboe', 'role': 'admin'},
            {'username': 'alpha.bah', 'email': 'alpha@interlinkglobal.edu', 'first_name': 'Alpha', 'last_name': 'Bah', 'role': 'instructor'},
            {'username': 'amadou.manneh', 'email': 'amadou@interlinkglobal.edu', 'first_name': 'Amadou', 'last_name': 'Manneh', 'role': 'instructor'},
            {'username': 'musa.jallow', 'email': 'musa@interlinkglobal.edu', 'first_name': 'Musa', 'last_name': 'Jallow', 'role': 'instructor'},
        ]
        
        for staff_data in staff_users:
            user, created = User.objects.get_or_create(
                username=staff_data['username'],
                defaults={
                    'email': staff_data['email'],
                    'first_name': staff_data['first_name'],
                    'last_name': staff_data['last_name'],
                    'is_staff': True
                }
            )
            if created:
                user.set_password('staff123')
                user.save()
                
                # Create user profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': staff_data['role']}
                )
                BaseSeeder.print_success(f"Created staff user: {staff_data['username']}")
        
        # Create regular users
        regular_users = [
            {'username': 'fatou.jallow', 'email': 'fatou@example.com', 'first_name': 'Fatou', 'last_name': 'Jallow', 'role': 'student'},
            {'username': 'modou.sanneh', 'email': 'modou@example.com', 'first_name': 'Modou', 'last_name': 'Sanneh', 'role': 'student'},
            {'username': 'aminata.barry', 'email': 'aminata@example.com', 'first_name': 'Aminata', 'last_name': 'Barry', 'role': 'student'},
            {'username': 'kebba.marong', 'email': 'kebba@example.com', 'first_name': 'Kebba', 'last_name': 'Marong', 'role': 'student'},
            {'username': 'lamin.fatty', 'email': 'lamin@example.com', 'first_name': 'Lamin', 'last_name': 'Fatty', 'role': 'student'},
        ]
        
        for user_data in regular_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password('student123')
                user.save()
                
                # Create user profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': user_data['role']}
                )
                BaseSeeder.print_success(f"Created user: {user_data['username']}")
        
        BaseSeeder.print_success(f"✅ Users seeding completed!")