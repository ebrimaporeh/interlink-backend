# seeder/seed_resources.py
from resources.models import ResourceCategory, Resource
from . import BaseSeeder

class SeedResources(BaseSeeder):
    @staticmethod
    def run():
        print("\n📄 Seeding Resources...")
        
        BaseSeeder.clear_model(Resource)
        BaseSeeder.clear_model(ResourceCategory)
        
        # Create categories
        categories_data = [
            {'name': 'Lecture Notes', 'icon': 'FaFileAlt', 'color': '#083750', 'order': 1},
            {'name': 'Assignments', 'icon': 'FaFileWord', 'color': '#3b82f6', 'order': 2},
            {'name': 'Past Exams', 'icon': 'FaFilePdf', 'color': '#ef4444', 'order': 3},
            {'name': 'Presentation Slides', 'icon': 'FaFilePowerpoint', 'color': '#f59e0b', 'order': 4},
            {'name': 'Video Tutorials', 'icon': 'FaVideo', 'color': '#8b5cf6', 'order': 5},
            {'name': 'E-Books', 'icon': 'FaFilePdf', 'color': '#10b981', 'order': 6},
        ]
        
        category_objs = {}
        for cat_data in categories_data:
            category = ResourceCategory.objects.create(
                name=cat_data['name'],
                slug=cat_data['name'].lower().replace(' ', '-'),
                icon=cat_data['icon'],
                color=cat_data['color'],
                order=cat_data['order'],
                is_active=True
            )
            category_objs[cat_data['name']] = category
            BaseSeeder.print_success(f"Created category: {category.name}")
        
        # Create resources
        resources_data = [
            {
                'title': 'Introduction to Computers - Lecture 1',
                'category': 'Lecture Notes',
                'description': 'Comprehensive notes covering computer hardware, software, and basic operations.',
                'file_type': 'pdf',
                'file_size': '2.4 MB',
                'author': 'Mr. Alpha Bah',
                'difficulty_level': 'beginner',
                'tags': ['Hardware', 'Software', 'Basics'],
                'order': 1,
                'is_featured': True
            },
            {
                'title': 'HTML5 & CSS3 Complete Guide',
                'category': 'E-Books',
                'description': 'Comprehensive guide to building modern websites with HTML5 and CSS3.',
                'file_type': 'pdf',
                'file_size': '5.7 MB',
                'author': 'Mr. Alieu Camara',
                'difficulty_level': 'beginner',
                'tags': ['HTML', 'CSS', 'Web Design'],
                'order': 2,
                'is_featured': True
            },
            {
                'title': 'JavaScript Fundamentals',
                'category': 'Lecture Notes',
                'description': 'Learn JavaScript from scratch with practical examples and exercises.',
                'file_type': 'pdf',
                'file_size': '3.8 MB',
                'author': 'Mr. Alieu Camara',
                'difficulty_level': 'intermediate',
                'tags': ['JavaScript', 'Programming', 'Web Dev'],
                'order': 3,
                'is_featured': True
            },
            {
                'title': 'Python Programming Exercises',
                'category': 'Assignments',
                'description': '100+ Python programming exercises for beginners to advanced level.',
                'file_type': 'pdf',
                'file_size': '2.1 MB',
                'author': 'Mr. Alpha Bah',
                'difficulty_level': 'intermediate',
                'tags': ['Python', 'Exercises', 'Programming'],
                'order': 4,
                'is_featured': False
            },
            {
                'title': 'Network Security Basics',
                'category': 'Lecture Notes',
                'description': 'Introduction to network security concepts, threats, and protection measures.',
                'file_type': 'pdf',
                'file_size': '3.9 MB',
                'author': 'Mr. Omar Ceesay',
                'difficulty_level': 'intermediate',
                'tags': ['Network', 'Security', 'Firewall'],
                'order': 5,
                'is_featured': True
            },
            {
                'title': 'Photoshop CC 2025 Guide',
                'category': 'E-Books',
                'description': 'Complete guide to Adobe Photoshop CC with practical design projects.',
                'file_type': 'pdf',
                'file_size': '12.5 MB',
                'author': 'Mr. Amadou Manneh',
                'difficulty_level': 'beginner',
                'tags': ['Photoshop', 'Design', 'Adobe'],
                'order': 6,
                'is_featured': True
            },
            {
                'title': 'Mid-Term Examination - Python',
                'category': 'Past Exams',
                'description': 'Past mid-term examination paper with answers.',
                'file_type': 'pdf',
                'file_size': '1.5 MB',
                'author': 'Mr. Alpha Bah',
                'difficulty_level': 'intermediate',
                'tags': ['Exam', 'Python', 'Assessment'],
                'order': 7,
                'is_featured': False
            },
            {
                'title': 'React.js Workshop Materials',
                'category': 'Presentation Slides',
                'description': 'Complete React.js workshop materials including code examples and projects.',
                'file_type': 'powerpoint',
                'file_size': '8.2 MB',
                'author': 'Mr. Alieu Camara',
                'difficulty_level': 'advanced',
                'tags': ['React', 'Frontend', 'JavaScript'],
                'order': 8,
                'is_featured': False
            },
            {
                'title': 'Database Management Systems',
                'category': 'Lecture Notes',
                'description': 'Complete guide to SQL and database design principles.',
                'file_type': 'pdf',
                'file_size': '4.5 MB',
                'author': 'Mr. Momodou Darboe',
                'difficulty_level': 'intermediate',
                'tags': ['SQL', 'Databases', 'Design'],
                'order': 9,
                'is_featured': False
            },
            {
                'title': 'English Grammar Handbook',
                'category': 'E-Books',
                'description': 'Complete guide to English grammar, punctuation, and writing style.',
                'file_type': 'pdf',
                'file_size': '3.2 MB',
                'author': 'Ms. Fatou Jallow',
                'difficulty_level': 'beginner',
                'tags': ['Grammar', 'Writing', 'English'],
                'order': 10,
                'is_featured': False
            }
        ]
        
        for resource_data in resources_data:
            category = category_objs[resource_data['category']]
            
            # Create the resource
            resource = Resource.objects.create(
                title=resource_data['title'],
                slug=resource_data['title'].lower().replace(' ', '-'),
                category=category,
                description=resource_data['description'],
                short_description=resource_data['description'][:200],
                file_type=resource_data['file_type'],
                file_size=resource_data['file_size'],
                author=resource_data['author'],
                difficulty_level=resource_data['difficulty_level'],
                order=resource_data['order'],
                is_featured=resource_data['is_featured'],
                is_active=True
            )
            
            # Add tags
            for tag in resource_data['tags']:
                resource.tags.add(tag)
            
            BaseSeeder.print_info(f"  Created resource: {resource.title}")
        
        BaseSeeder.print_success(f"✅ Resources seeding completed! Created {len(resources_data)} resources")