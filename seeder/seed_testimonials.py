# seeder/seed_testimonials.py
from content.models import Testimonial
from . import BaseSeeder

class SeedTestimonials(BaseSeeder):
    @staticmethod
    def run():
        print("\n💬 Seeding Testimonials...")
        
        BaseSeeder.clear_model(Testimonial)
        
        testimonials_data = [
            {
                'name': 'Fatou Jallow',
                'course': 'Web Development Bootcamp',
                'content': 'The Web Development Bootcamp completely changed my career. I landed a job as a junior developer just two months after completing the course. The instructors are outstanding!',
                'rating': 5,
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'Modou Sanneh',
                'course': 'Diploma in IT & Business Computing',
                'content': 'I started with zero computer knowledge and graduated with a full diploma. Interlink\'s teaching style is patient, practical, and incredibly effective. I\'m now working in IT support.',
                'rating': 5,
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'Aminata Barry',
                'course': 'Professional Graphic Design',
                'content': 'The graphic design program was well-structured and immediately applicable. I now freelance for three companies and have grown my own studio. Best decision I ever made.',
                'rating': 5,
                'is_featured': True,
                'order': 3
            },
            {
                'name': 'Kebba Marong',
                'course': 'Python Programming Essentials',
                'content': 'The Python course gave me the skills I needed to transition into data analysis. The practical projects were especially valuable for my portfolio.',
                'rating': 4,
                'is_featured': False,
                'order': 4
            },
            {
                'name': 'Mariama Njie',
                'course': 'Cybersecurity Awareness',
                'content': 'This course opened my eyes to the importance of cybersecurity. I\'ve implemented many of the practices at my company.',
                'rating': 5,
                'is_featured': False,
                'order': 5
            }
        ]
        
        for testimonial_data in testimonials_data:
            Testimonial.objects.create(
                name=testimonial_data['name'],
                course=testimonial_data['course'],
                content=testimonial_data['content'],
                rating=testimonial_data['rating'],
                is_featured=testimonial_data['is_featured'],
                order=testimonial_data['order'],
                is_active=True
            )
            BaseSeeder.print_success(f"Created testimonial from: {testimonial_data['name']}")
        
        BaseSeeder.print_success(f"✅ Testimonials seeding completed! Created {len(testimonials_data)} testimonials")