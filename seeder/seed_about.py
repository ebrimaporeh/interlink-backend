# seeder/seed_about.py
from content.models import AboutPage, Achievement, Partner, FAQ
from . import BaseSeeder

class SeedAbout(BaseSeeder):
    @staticmethod
    def run():
        print("\n📖 Seeding About Page Content...")
        
        BaseSeeder.clear_model(AboutPage)
        BaseSeeder.clear_model(Achievement)
        BaseSeeder.clear_model(Partner)
        BaseSeeder.clear_model(FAQ)
        
        # Create About Page
        about, created = AboutPage.objects.get_or_create(
            id=1,
            defaults={
                'title': 'About Interlink Global College',
                'subtitle': 'Empowering Digital Futures Since 2015',
                'mission': 'To provide accessible, high-quality digital education that prepares students for successful careers in technology. We strive to create an inclusive learning environment where everyone can discover their potential.',
                'vision': 'To be the leading institution in The Gambia for technology education, producing skilled professionals who drive innovation and economic growth across Africa.',
                'stats': [
                    {'number': '1,200', 'label': 'Graduates'},
                    {'number': '45', 'label': 'Expert Teachers'},
                    {'number': '12', 'label': 'Programs'},
                    {'number': '98', 'label': 'Satisfaction'}
                ],
                'core_values': [
                    {'title': 'Excellence', 'description': 'We maintain the highest standards in education.', 'icon': 'FaCheckCircle'},
                    {'title': 'Inclusivity', 'description': 'Education accessible to everyone.', 'icon': 'FaUsers'},
                    {'title': 'Integrity', 'description': 'Transparent and ethical practices.', 'icon': 'FaHandshake'},
                    {'title': 'Innovation', 'description': 'Continuous curriculum updates.', 'icon': 'FaRocket'}
                ]
            }
        )
        BaseSeeder.print_success("Created About Page content")
        
        # Create Achievements
        achievements_data = [
            {'year': 2015, 'title': 'College Founded', 'description': 'Interlink Global College opened its doors with just 50 students.', 'order': 1},
            {'year': 2017, 'title': 'First Graduation', 'description': 'Celebrated our first cohort of 120 graduates.', 'order': 2},
            {'year': 2019, 'title': 'Campus Expansion', 'description': 'Moved to our current state-of-the-art facility.', 'order': 3},
            {'year': 2021, 'title': 'Online Learning Launch', 'description': 'Introduced hybrid learning options.', 'order': 4},
            {'year': 2023, 'title': 'Industry Partnerships', 'description': '25+ tech company partnerships established.', 'order': 5},
            {'year': 2025, 'title': '1000+ Graduates', 'description': 'Milestone of 1000 successful graduates reached.', 'order': 6}
        ]
        
        for ach_data in achievements_data:
            Achievement.objects.create(
                year=ach_data['year'],
                title=ach_data['title'],
                description=ach_data['description'],
                order=ach_data['order'],
                is_active=True
            )
            BaseSeeder.print_info(f"  Created achievement: {ach_data['year']} - {ach_data['title']}")
        
        # Create Partners
        partners_data = [
            {'name': 'Microsoft', 'website': 'https://microsoft.com', 'order': 1},
            {'name': 'Google', 'website': 'https://google.com', 'order': 2},
            {'name': 'Cisco', 'website': 'https://cisco.com', 'order': 3},
            {'name': 'Adobe', 'website': 'https://adobe.com', 'order': 4},
            {'name': 'Oracle', 'website': 'https://oracle.com', 'order': 5},
            {'name': 'IBM', 'website': 'https://ibm.com', 'order': 6}
        ]
        
        for partner_data in partners_data:
            Partner.objects.create(
                name=partner_data['name'],
                website=partner_data['website'],
                order=partner_data['order'],
                is_active=True
            )
            BaseSeeder.print_info(f"  Created partner: {partner_data['name']}")
        
        # Create FAQs
        faqs_data = [
            {'question': 'How long does it take to complete a program?', 'answer': 'Program durations vary from 6 weeks for short courses to 12 months for advanced diplomas.', 'category': 'Admissions', 'order': 1},
            {'question': 'Do you offer online classes?', 'answer': 'Yes! We offer both in-person and hybrid learning options.', 'category': 'Admissions', 'order': 2},
            {'question': 'What are the admission requirements?', 'answer': 'Requirements vary by program. Most certificate programs only require basic literacy.', 'category': 'Admissions', 'order': 3},
            {'question': 'Do you provide job placement assistance?', 'answer': 'Yes, we have dedicated career services for resume writing and job placement.', 'category': 'Career', 'order': 4},
            {'question': 'Can I pay in installments?', 'answer': 'Yes, we offer flexible payment plans to make education accessible.', 'category': 'Payments', 'order': 5}
        ]
        
        for faq_data in faqs_data:
            FAQ.objects.create(
                question=faq_data['question'],
                answer=faq_data['answer'],
                category=faq_data['category'],
                order=faq_data['order'],
                is_active=True
            )
            BaseSeeder.print_info(f"  Created FAQ: {faq_data['question'][:50]}...")
        
        BaseSeeder.print_success(f"✅ About page seeding completed!")