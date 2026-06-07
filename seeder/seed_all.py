# seeder/seed_all.py
from .seed_courses import SeedCourses
from .seed_team import SeedTeam
from .seed_testimonials import SeedTestimonials
from .seed_policies import SeedPolicies
from .seed_resources import SeedResources
from .seed_about import SeedAbout
from .seed_gallery import SeedGallery
from .seed_blog import SeedBlog
from .seed_users import SeedUsers

class SeedAll:
    @staticmethod
    def run():
        print("\n" + "="*60)
        print("🌱 STARTING DATABASE SEEDING")
        print("="*60)
        
        # Run all seeders in order (dependencies matter)
        SeedUsers.run()           # Users first
        SeedCourses.run()         # Courses depend on nothing
        SeedTeam.run()            # Team members
        SeedTestimonials.run()    # Testimonials
        SeedPolicies.run()        # Policies
        SeedResources.run()       # Resources
        SeedAbout.run()           # About page (has achievements, partners, FAQs)
        SeedGallery.run()         # Gallery
        SeedBlog.run()            # Blog posts
        
        print("\n" + "="*60)
        print("🎉 DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)