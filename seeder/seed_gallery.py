# seeder/seed_gallery.py
from content.models import GalleryCategory, GalleryItem
from . import BaseSeeder

class SeedGallery(BaseSeeder):
    @staticmethod
    def run():
        print("\n🖼️ Seeding Gallery...")
        
        BaseSeeder.clear_model(GalleryItem)
        BaseSeeder.clear_model(GalleryCategory)
        
        # Create categories
        categories_data = [
            {'name': 'Campus Life', 'slug': 'campus-life', 'order': 1},
            {'name': 'Students', 'slug': 'students', 'order': 2},
            {'name': 'Events', 'slug': 'events', 'order': 3},
            {'name': 'Facilities', 'slug': 'facilities', 'order': 4},
        ]
        
        category_objs = {}
        for cat_data in categories_data:
            category = GalleryCategory.objects.create(
                name=cat_data['name'],
                slug=cat_data['slug'],
                order=cat_data['order'],
                is_active=True
            )
            category_objs[cat_data['name']] = category
            BaseSeeder.print_success(f"Created category: {category.name}")
        
        # Gallery items data
        gallery_images = [
            {'caption': 'Computer Lab', 'sub': '50+ modern workstations', 'category': 'Facilities', 'url': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800&q=85'},
            {'caption': 'Collaboration', 'sub': 'Group learning sessions', 'category': 'Students', 'url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=85'},
            {'caption': 'Coding Class', 'sub': 'Hands-on programming', 'category': 'Students', 'url': 'https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800&q=85'},
            {'caption': 'Graduation Day', 'sub': 'Celebrating our graduates', 'category': 'Events', 'url': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800&q=85'},
            {'caption': 'Design Workshop', 'sub': 'Creative sessions in action', 'category': 'Events', 'url': 'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800&q=85'},
            {'caption': 'Expert Instruction', 'sub': 'Industry-certified tutors', 'category': 'Students', 'url': 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&q=85'},
            {'caption': 'Web Dev Bootcamp', 'sub': 'Building real projects', 'category': 'Students', 'url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=85'},
            {'caption': 'Study Groups', 'sub': 'Peer-to-peer learning', 'category': 'Students', 'url': 'https://images.unsplash.com/photo-1544531585-9847b68c8c86?w=800&q=85'},
            {'caption': 'Team Projects', 'sub': 'Real-world experience', 'category': 'Students', 'url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&q=85'},
            {'caption': 'Certificate Ceremony', 'sub': 'Moments of achievement', 'category': 'Events', 'url': 'https://images.unsplash.com/photo-1543269865-cbf427effbad?w=800&q=85'},
            {'caption': 'Modern Library', 'sub': 'Quiet study spaces', 'category': 'Facilities', 'url': 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=800&q=85'},
            {'caption': 'Tech Lab', 'sub': 'Latest equipment', 'category': 'Facilities', 'url': 'https://images.unsplash.com/photo-1581092335871-4c4a9c8f2b8a?w=800&q=85'},
        ]
        
        for idx, img_data in enumerate(gallery_images):
            category = category_objs[img_data['category']]
            
            item = GalleryItem.objects.create(
                title=img_data['caption'],
                caption=img_data['caption'],
                category=category,
                media_type='image',
                order=idx,
                is_active=True,
                is_featured=idx < 6
            )
            
            # Download and set image
            image_file = BaseSeeder.download_image(img_data['url'])
            if image_file:
                BaseSeeder.save_image(item.image, f"gallery_{idx}.jpg", image_file)
            
            BaseSeeder.print_info(f"  Created gallery item: {img_data['caption']}")
        
        # Create video items
        video_items = [
            {'caption': 'Campus Tour', 'sub': 'See our facilities', 'video_url': 'https://www.youtube.com/watch?v=example1', 'category': 'Campus Life'},
            {'caption': 'Student Life', 'sub': 'A day at Interlink', 'video_url': 'https://www.youtube.com/watch?v=example2', 'category': 'Campus Life'},
            {'caption': 'Graduation Ceremony 2024', 'sub': 'Celebrating success', 'video_url': 'https://www.youtube.com/watch?v=example3', 'category': 'Events'},
        ]
        
        for idx, video_data in enumerate(video_items):
            category = category_objs[video_data['category']]
            GalleryItem.objects.create(
                title=video_data['caption'],
                caption=video_data['caption'],
                category=category,
                media_type='video',
                video_url=video_data['video_url'],
                order=len(gallery_images) + idx,
                is_active=True,
                is_featured=False
            )
            BaseSeeder.print_info(f"  Created video: {video_data['caption']}")
        
        BaseSeeder.print_success(f"✅ Gallery seeding completed! Created {len(gallery_images)} images and {len(video_items)} videos")