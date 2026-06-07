# seeder/seed_courses.py
from courses.models import CourseCategory, Course, CourseModule, CourseLesson
from . import BaseSeeder

class SeedCourses(BaseSeeder):
    @staticmethod
    def run():
        print("\n📚 Seeding Courses...")
        
        # Clear existing data
        BaseSeeder.clear_model(CourseLesson)
        BaseSeeder.clear_model(CourseModule)
        BaseSeeder.clear_model(Course)
        BaseSeeder.clear_model(CourseCategory)
        
        # Create Categories
        categories = [
            {'name': 'Computer Literacy', 'icon': 'Monitor', 'order': 1, 'description': 'Foundational computer skills for beginners'},
            {'name': 'Web Development', 'icon': 'Globe', 'order': 2, 'description': 'Build modern websites and web applications'},
            {'name': 'Programming', 'icon': 'Code', 'order': 3, 'description': 'Learn programming languages and concepts'},
            {'name': 'Design', 'icon': 'Palette', 'order': 4, 'description': 'Graphic and UI/UX design courses'},
            {'name': 'Cybersecurity', 'icon': 'Shield', 'order': 5, 'description': 'Protect systems and data from threats'},
            {'name': 'English', 'icon': 'BookOpen', 'order': 6, 'description': 'English language and communication skills'},
        ]
        
        category_objs = {}
        for cat in categories:
            obj, created = CourseCategory.objects.get_or_create(
                name=cat['name'],
                defaults={
                    'slug': cat['name'].lower().replace(' ', '-'),
                    'icon': cat['icon'],
                    'order': cat['order'],
                    'description': cat['description'],
                    'is_active': True
                }
            )
            category_objs[cat['name']] = obj
            BaseSeeder.print_success(f"Created category: {cat['name']}")
        
        # Create Courses
        courses_data = [
            {
                'title': 'Certificate in Computer Literacy',
                'category': 'Computer Literacy',
                'level': 'certificate',
                'duration': '3 Months',
                'price': 'D3,500',
                'price_number': 3500,
                'short_description': 'Master the essentials of computing: operating systems, productivity suites, and internet skills.',
                'description': 'This comprehensive certificate program covers all fundamental computer skills needed for modern workplace efficiency.',
                'modules': ['Windows OS', 'MS Office', 'Internet', 'Email', 'File Management'],
                'learning_outcomes': ['Navigate Windows OS confidently', 'Create professional documents in MS Word', 'Build spreadsheets in Excel', 'Create presentations in PowerPoint', 'Use email professionally'],
                'image': 'https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=800&q=80',
                'banner_icon': 'Monitor',
                'order': 1,
                'is_featured': True
            },
            {
                'title': 'Diploma in IT & Business Computing',
                'category': 'Computer Literacy',
                'level': 'diploma',
                'duration': '6 Months',
                'price': 'D6,000',
                'price_number': 6000,
                'short_description': 'Comprehensive diploma blending IT with practical business applications.',
                'description': 'This diploma combines information technology with business applications and project management fundamentals.',
                'modules': ['Databases', 'Networking', 'Spreadsheets', 'Presentations', 'Business Communication'],
                'learning_outcomes': ['Design and manage databases', 'Configure basic networks', 'Analyze data with spreadsheets', 'Create professional presentations', 'Communicate effectively in business'],
                'image': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80',
                'banner_icon': 'BarChart',
                'order': 2,
                'is_featured': True
            },
            {
                'title': 'Advanced Diploma in Information Technology',
                'category': 'Computer Literacy',
                'level': 'advanced_diploma',
                'duration': '12 Months',
                'price': 'D10,500',
                'price_number': 10500,
                'short_description': 'Deep-dive advanced qualification covering hardware, software engineering, and systems administration.',
                'description': 'Advanced program for serious IT professionals covering system administration, cloud computing, and network security.',
                'modules': ['System Admin', 'Cloud Computing', 'Linux', 'Network Security', 'Virtualization'],
                'learning_outcomes': ['Administer Windows and Linux servers', 'Deploy cloud solutions', 'Implement network security', 'Manage virtualization platforms', 'Troubleshoot complex IT issues'],
                'image': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80',
                'banner_icon': 'Rocket',
                'order': 3,
                'is_featured': False
            },
            {
                'title': 'Web Development Bootcamp',
                'category': 'Web Development',
                'level': 'programming',
                'duration': '5 Months',
                'price': 'D7,500',
                'price_number': 7500,
                'short_description': 'Build modern, responsive websites and web apps with popular frameworks.',
                'description': 'Intensive bootcamp covering full-stack web development from HTML/CSS to React and Node.js.',
                'modules': ['HTML/CSS', 'JavaScript', 'React', 'Node.js', 'MongoDB'],
                'learning_outcomes': ['Build responsive websites', 'Create interactive front-end applications', 'Develop REST APIs', 'Work with databases', 'Deploy web applications'],
                'image': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=80',
                'banner_icon': 'Globe',
                'order': 4,
                'is_featured': True
            },
            {
                'title': 'Python Programming Essentials',
                'category': 'Programming',
                'level': 'programming',
                'duration': '4 Months',
                'price': 'D6,500',
                'price_number': 6500,
                'short_description': 'From fundamentals to practical applications for data analysis and automation.',
                'description': 'Learn Python from scratch with hands-on projects in data analysis, automation, and scripting.',
                'modules': ['Python 3', 'Data Structures', 'Automation', 'File Handling', 'APIs'],
                'learning_outcomes': ['Write Python scripts', 'Work with data structures', 'Automate repetitive tasks', 'Handle files and exceptions', 'Consume REST APIs'],
                'image': 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&q=80',
                'banner_icon': 'Terminal',
                'order': 5,
                'is_featured': False
            },
            {
                'title': 'Professional Graphic Design',
                'category': 'Design',
                'level': 'design',
                'duration': '4 Months',
                'price': 'D6,000',
                'price_number': 6000,
                'short_description': 'Master Adobe Creative Suite and develop a strong design portfolio.',
                'description': 'Comprehensive graphic design course covering Photoshop, Illustrator, InDesign, and branding principles.',
                'modules': ['Photoshop', 'Illustrator', 'InDesign', 'Branding', 'Typography'],
                'learning_outcomes': ['Create professional graphics', 'Design logos and branding materials', 'Layout print publications', 'Understand color theory', 'Build a professional portfolio'],
                'image': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800&q=80',
                'banner_icon': 'Palette',
                'order': 6,
                'is_featured': True
            },
            {
                'title': 'English Language Course',
                'category': 'English',
                'level': 'english',
                'duration': '3 Months',
                'price': 'D4,000',
                'price_number': 4000,
                'short_description': 'Develop strong written and spoken English skills for professional environments.',
                'description': 'Improve your English communication skills for professional and academic success.',
                'modules': ['Grammar', 'Business Writing', 'Speaking', 'Vocabulary', 'Presentation Skills'],
                'learning_outcomes': ['Write professional emails', 'Speak confidently in meetings', 'Understand business vocabulary', 'Give presentations', 'Improve grammar'],
                'image': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&q=80',
                'banner_icon': 'BookOpenCheck',
                'order': 7,
                'is_featured': False
            },
            {
                'title': 'Typing & MS Office Essentials',
                'category': 'Computer Literacy',
                'level': 'short_course',
                'duration': '6 Weeks',
                'price': 'D2,500',
                'price_number': 2500,
                'short_description': 'Build speed and accuracy in typing while mastering Microsoft Office.',
                'description': 'Essential office skills including typing proficiency and complete MS Office mastery.',
                'modules': ['Word', 'Excel', 'PowerPoint', 'Typing', 'Outlook'],
                'learning_outcomes': ['Type 40+ WPM', 'Create professional documents', 'Build spreadsheets with formulas', 'Design presentations', 'Manage emails effectively'],
                'image': 'https://images.unsplash.com/photo-1581092335871-4c4a9c8f2b8a?w=800&q=80',
                'banner_icon': 'Zap',
                'order': 8,
                'is_featured': False
            },
            {
                'title': 'Cybersecurity Awareness',
                'category': 'Cybersecurity',
                'level': 'short_course',
                'duration': '8 Weeks',
                'price': 'D3,000',
                'price_number': 3000,
                'short_description': 'Understand online threats and data protection best practices.',
                'description': 'Essential cybersecurity knowledge for personal and business protection.',
                'modules': ['Threat Detection', 'Data Privacy', 'Password Security', 'Social Engineering', 'Safe Browsing'],
                'learning_outcomes': ['Identify phishing attempts', 'Protect personal data', 'Create strong passwords', 'Recognize security threats', 'Implement safe browsing habits'],
                'image': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80',
                'banner_icon': 'Shield',
                'order': 9,
                'is_featured': True
            }
        ]
        
        created_courses = []
        for course_data in courses_data:
            category = category_objs[course_data['category']]
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'slug': course_data['title'].lower().replace(' ', '-'),
                    'category': category,
                    'level': course_data['level'],
                    'duration': course_data['duration'],
                    'price': course_data['price'],
                    'price_number': course_data['price_number'],
                    'short_description': course_data['short_description'],
                    'description': course_data['description'],
                    'modules': course_data['modules'],
                    'learning_outcomes': course_data['learning_outcomes'],
                    'banner_icon': course_data['banner_icon'],
                    'order': course_data['order'],
                    'is_featured': course_data['is_featured'],
                    'is_active': True
                }
            )
            
            # Download and set image
            if course_data['image'] and not course.image:
                image_file = BaseSeeder.download_image(course_data['image'])
                if image_file:
                    BaseSeeder.save_image(course.image, f"{course.slug}.jpg", image_file)
            
            created_courses.append(course)
            BaseSeeder.print_success(f"Created course: {course.title}")
        
        # Create modules and lessons for specific courses
        for course in created_courses:
            if course.title == 'Web Development Bootcamp':
                modules_data = [
                    {
                        'title': 'HTML & CSS Fundamentals', 
                        'order': 1, 
                        'lessons': [
                            {'title': 'Introduction to HTML', 'content': 'Learn HTML basics', 'order': 1, 'duration_minutes': 30},
                            {'title': 'CSS Styling', 'content': 'Learn CSS properties', 'order': 2, 'duration_minutes': 45},
                            {'title': 'Responsive Design', 'content': 'Make sites mobile-friendly', 'order': 3, 'duration_minutes': 60}
                        ]
                    },
                    {
                        'title': 'JavaScript Basics', 
                        'order': 2, 
                        'lessons': [
                            {'title': 'Variables and Data Types', 'content': 'Learn JS variables', 'order': 1, 'duration_minutes': 40},
                            {'title': 'Functions and Arrays', 'content': 'Work with functions', 'order': 2, 'duration_minutes': 50},
                            {'title': 'DOM Manipulation', 'content': 'Interact with HTML', 'order': 3, 'duration_minutes': 55}
                        ]
                    },
                ]
                
                for module_data in modules_data:
                    module = CourseModule.objects.create(
                        course=course,
                        title=module_data['title'],
                        order=module_data['order'],
                        duration_hours=sum(l['duration_minutes'] for l in module_data['lessons']) // 60
                    )
                    
                    for lesson_data in module_data['lessons']:
                        CourseLesson.objects.create(
                            module=module,
                            title=lesson_data['title'],
                            content=lesson_data['content'],
                            order=lesson_data['order'],
                            duration_minutes=lesson_data['duration_minutes']
                        )
                    BaseSeeder.print_info(f"  Created module: {module.title} with {len(module_data['lessons'])} lessons")
            
            elif course.title == 'Python Programming Essentials':
                modules_data = [
                    {
                        'title': 'Python Fundamentals', 
                        'order': 1, 
                        'lessons': [
                            {'title': 'Python Installation and Setup', 'content': 'Install Python and set up development environment', 'order': 1, 'duration_minutes': 20},
                            {'title': 'Variables and Data Types', 'content': 'Learn about variables, strings, numbers, and booleans', 'order': 2, 'duration_minutes': 45},
                            {'title': 'Control Flow', 'content': 'If statements, loops, and conditionals', 'order': 3, 'duration_minutes': 50}
                        ]
                    },
                    {
                        'title': 'Data Structures', 
                        'order': 2, 
                        'lessons': [
                            {'title': 'Lists and Tuples', 'content': 'Working with sequences', 'order': 1, 'duration_minutes': 40},
                            {'title': 'Dictionaries and Sets', 'content': 'Key-value pairs and unique collections', 'order': 2, 'duration_minutes': 45},
                            {'title': 'List Comprehensions', 'content': 'Efficient list creation', 'order': 3, 'duration_minutes': 30}
                        ]
                    },
                ]
                
                for module_data in modules_data:
                    module = CourseModule.objects.create(
                        course=course,
                        title=module_data['title'],
                        order=module_data['order'],
                        duration_hours=sum(l['duration_minutes'] for l in module_data['lessons']) // 60
                    )
                    
                    for lesson_data in module_data['lessons']:
                        CourseLesson.objects.create(
                            module=module,
                            title=lesson_data['title'],
                            content=lesson_data['content'],
                            order=lesson_data['order'],
                            duration_minutes=lesson_data['duration_minutes']
                        )
                    BaseSeeder.print_info(f"  Created module: {module.title} with {len(module_data['lessons'])} lessons")
        
        BaseSeeder.print_success(f"✅ Courses seeding completed! Created {len(created_courses)} courses")