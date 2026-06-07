# seeder/seed_blog.py
from django.utils.text import slugify
from content.models import BlogCategory, BlogPost
from . import BaseSeeder

class SeedBlog(BaseSeeder):
    @staticmethod
    def run():
        print("\n📝 Seeding Blog...")
        
        BaseSeeder.clear_model(BlogPost)
        BaseSeeder.clear_model(BlogCategory)
        
        # Create categories
        categories_data = [
            {'name': 'Career Tips', 'slug': 'career-tips'},
            {'name': 'Web Development', 'slug': 'web-development'},
            {'name': 'College News', 'slug': 'college-news'},
            {'name': 'Student Success', 'slug': 'student-success'},
            {'name': 'Tech Trends', 'slug': 'tech-trends'},
            {'name': 'Design', 'slug': 'design'},
        ]
        
        category_objs = {}
        for cat_data in categories_data:
            category = BlogCategory.objects.create(
                name=cat_data['name'],
                slug=cat_data['slug'],
                is_active=True
            )
            category_objs[cat_data['name']] = category
            BaseSeeder.print_success(f"Created category: {category.name}")
        
        # Blog posts
        posts_data = [
            {
                'title': '5 Essential Tech Skills Employers Are Looking for in 2025',
                'category': 'Career Tips',
                'author': 'Kebba Marong',
                'excerpt': 'The job market is evolving fast. Here are the most in-demand digital skills that will give you a competitive edge this year and beyond.',
                'content': 'Full article content here... The technology landscape is changing faster than ever...',
                'tags': 'Career, Skills, Technology',
                'read_time': 5,
                'is_featured': True,
                'image': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&q=80'
            },
            {
                'title': 'Why Every Business Needs a Mobile-Friendly Website in 2025',
                'category': 'Web Development',
                'author': 'Lamin Fatty',
                'excerpt': 'Mobile internet usage now accounts for over 60% of all web traffic. Here\'s why responsive design is no longer optional.',
                'content': 'Full article content here... Mobile devices have become the primary way people access the internet...',
                'tags': 'Web Design, Mobile, Responsive',
                'read_time': 4,
                'is_featured': True,
                'image': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80'
            },
            {
                'title': 'Interlink Celebrates Record 300 Graduates at Annual Ceremony',
                'category': 'College News',
                'author': 'Admin Team',
                'excerpt': 'This year\'s graduation ceremony was our biggest yet, with 300 students receiving their certificates and diplomas.',
                'content': 'Full article content here... Interlink Global College hosted its largest graduation ceremony...',
                'tags': 'Graduation, Achievement, Community',
                'read_time': 3,
                'is_featured': True,
                'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&q=80'
            },
            {
                'title': '10 Tips for Landing Your First Tech Job',
                'category': 'Career Tips',
                'author': 'Fatou Jallow',
                'excerpt': 'Breaking into tech can be challenging. These practical tips will help you stand out to employers.',
                'content': 'Full article content here... Breaking into tech requires strategy and persistence...',
                'tags': 'Job Search, Career, Interview',
                'read_time': 7,
                'is_featured': False,
                'image': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&q=80'
            },
            {
                'title': 'The Rise of AI in Web Development',
                'category': 'Tech Trends',
                'author': 'Alpha Bah',
                'excerpt': 'How artificial intelligence is transforming the way we build websites and applications.',
                'content': 'Full article content here... AI is revolutionizing web development...',
                'tags': 'AI, Web Development, Technology',
                'read_time': 6,
                'is_featured': False,
                'image': 'https://images.unsplash.com/photo-1488229297570-58520851e868?w=800&q=80'
            },
            {
                'title': 'Student Spotlight: From Beginner to Professional Developer',
                'category': 'Student Success',
                'author': 'Aminata Barry',
                'excerpt': 'Meet Modou Jallow, who went from knowing nothing about coding to landing a job as a junior developer.',
                'content': 'Full article content here... Modou\'s journey is an inspiration to all...',
                'tags': 'Success Story, Student, Inspiration',
                'read_time': 5,
                'is_featured': False,
                'image': 'https://images.unsplash.com/photo-1543269865-cbf427effbad?w=800&q=80'
            }
        ]
        
        for post_data in posts_data:
            category = category_objs[post_data['category']]
            
            post = BlogPost.objects.create(
                title=post_data['title'],
                slug=slugify(post_data['title'])[:200],
                category=category,
                author=post_data['author'],
                excerpt=post_data['excerpt'],
                content=post_data['content'],
                tags=post_data['tags'],
                read_time=post_data['read_time'],
                is_featured=post_data['is_featured'],
                is_published=True
            )
            
            # Download and set image
            image_file = BaseSeeder.download_image(post_data['image'])
            if image_file:
                BaseSeeder.save_image(post.featured_image, f"{post.slug}.jpg", image_file)
            
            BaseSeeder.print_info(f"  Created blog post: {post.title}")
        
        BaseSeeder.print_success(f"✅ Blog seeding completed! Created {len(posts_data)} blog posts")