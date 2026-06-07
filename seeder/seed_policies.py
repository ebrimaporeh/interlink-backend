# seeder/seed_policies.py
from content.models import PolicyCategory, Policy
from . import BaseSeeder

class SeedPolicies(BaseSeeder):
    @staticmethod
    def run():
        print("\n📋 Seeding Policies...")
        
        BaseSeeder.clear_model(Policy)
        BaseSeeder.clear_model(PolicyCategory)
        
        # Create categories
        categories_data = [
            {'name': 'School Policies', 'icon': 'FaUniversity', 'order': 1, 'description': 'General institutional policies'},
            {'name': 'NAQAA Policies', 'icon': 'FaShieldAlt', 'order': 2, 'description': 'Accreditation and quality assurance policies'},
            {'name': 'Classroom Rules', 'icon': 'FaChalkboardTeacher', 'order': 3, 'description': 'Rules for classroom conduct'},
            {'name': 'Student Code of Conduct', 'icon': 'FaUserGraduate', 'order': 4, 'description': 'Student behavior expectations'},
            {'name': 'Academic Policies', 'icon': 'FaBook', 'order': 5, 'description': 'Grading and academic standards'},
            {'name': 'Health & Safety', 'icon': 'FaHeartbeat', 'order': 6, 'description': 'Health and safety guidelines'},
        ]
        
        category_objs = {}
        for cat_data in categories_data:
            category = PolicyCategory.objects.create(
                name=cat_data['name'],
                slug=cat_data['name'].lower().replace(' ', '-'),
                icon=cat_data['icon'],
                order=cat_data['order'],
                description=cat_data['description'],
                is_active=True
            )
            category_objs[cat_data['name']] = category
            BaseSeeder.print_success(f"Created category: {category.name}")
        
        # Create policies
        policies_data = {
            'School Policies': [
                {'title': 'Admissions Policy', 'content': 'Open admission to all qualified individuals regardless of race, color, religion, gender, or national origin. Minimum requirements: completion of secondary education or equivalent.', 'order': 1},
                {'title': 'Fees and Payment Policy', 'content': 'Tuition fees due before semester commencement. Installment plans available (50% upfront, balance within 60 days). Late payment penalty: D100 per week after grace period.', 'order': 2},
                {'title': 'Attendance Policy', 'content': 'Minimum 80% attendance required for certification. Late arrivals exceeding 15 minutes marked as absent. Medical emergencies require doctor\'s note.', 'order': 3},
                {'title': 'Privacy and Data Protection', 'content': 'Student records protected under Data Privacy Act. Information shared only with explicit consent or legal requirement.', 'order': 4}
            ],
            'NAQAA Policies': [
                {'title': 'Accreditation Standards', 'content': 'Compliance with National Qualifications Framework (NQF). Regular curriculum review and update cycle. Qualified instructors with minimum bachelor\'s degree.', 'order': 1},
                {'title': 'Assessment and Grading Policy', 'content': 'Continuous assessment: 40%, final examination: 60%. Grading scale: A (80-100%), B (70-79%), C (60-69%), D (50-59%), F (below 50%).', 'order': 2},
                {'title': 'Quality Assurance Mechanisms', 'content': 'Internal quality assurance committee. Student feedback collection each semester. Annual self-assessment report submitted.', 'order': 3}
            ],
            'Classroom Rules': [
                {'title': 'General Conduct', 'content': 'Arrive on time and prepared for class. Show respect to instructors and fellow students. No disruptive behavior during lectures.', 'order': 1},
                {'title': 'Electronics Policy', 'content': 'Laptops only for class-related activities. Mobile phones must be silent and stored away. No headphones during lectures.', 'order': 2},
                {'title': 'Computer Lab Rules', 'content': 'No installation of unauthorized software. Save work frequently. Log off after each session.', 'order': 3}
            ],
            'Student Code of Conduct': [
                {'title': 'Academic Integrity', 'content': 'No plagiarism, cheating, or unauthorized collaboration. Proper citation of all sources in assignments.', 'order': 1},
                {'title': 'Respect for Diversity', 'content': 'Respect all cultures, religions, and backgrounds. No discrimination or harassment tolerated.', 'order': 2},
                {'title': 'Dress Code', 'content': 'Business casual attire appropriate for learning. No offensive or inappropriate graphics/text.', 'order': 3}
            ],
            'Academic Policies': [
                {'title': 'Grading System', 'content': 'A (80-100%): Excellent, B (70-79%): Good, C (60-69%): Satisfactory, D (50-59%): Passing, F (below 50%): Fail.', 'order': 1},
                {'title': 'Examination Policies', 'content': 'No communication between students during exams. No unauthorized materials in exam hall. Arrive 15 minutes before exam start.', 'order': 2},
                {'title': 'Graduation Requirements', 'content': 'Complete all required courses with passing grades. Minimum GPA of 2.0 for graduation.', 'order': 3}
            ],
            'Health & Safety': [
                {'title': 'Emergency Procedures', 'content': 'Fire drills conducted monthly. Evacuation routes posted in all rooms. Assembly point: Main parking lot.', 'order': 1},
                {'title': 'Campus Security', 'content': 'Security personnel on duty 24/7. CCTV surveillance in common areas. Student ID required after 6 PM.', 'order': 2},
                {'title': 'Mental Health Support', 'content': 'Counseling services available free. Confidential mental health support. Stress management workshops offered.', 'order': 3}
            ]
        }
        
        total_policies = 0
        for category_name, policies in policies_data.items():
            category = category_objs[category_name]
            for policy_data in policies:
                Policy.objects.create(
                    category=category,
                    title=policy_data['title'],
                    content=policy_data['content'],
                    order=policy_data['order'],
                    is_active=True
                )
                total_policies += 1
                BaseSeeder.print_info(f"  Created policy: {policy_data['title']}")
        
        BaseSeeder.print_success(f"✅ Policies seeding completed! Created {total_policies} policies")