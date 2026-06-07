# seeder/seed_team.py
from content.models import TeamMember
from . import BaseSeeder

class SeedTeam(BaseSeeder):
    @staticmethod
    def run():
        print("\n👥 Seeding Team Members...")
        
        BaseSeeder.clear_model(TeamMember)
        
        team_data = [
            {
                'name': 'Mr. Momodou Darboe',
                'position': 'CEO & Founder',
                'bio': 'Visionary leader with 15+ years in digital education. Momodou founded Interlink Global College with a mission to democratize quality tech education in The Gambia.',
                'email': 'momodou@interlinkglobal.edu',
                'expertise': ['Leadership', 'Strategic Planning', 'Education Technology'],
                'order': 1,
                'image': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&q=80'
            },
            {
                'name': 'Mr. Alpha Bah',
                'position': 'Senior IT Instructor',
                'bio': 'Certified IT professional specializing in network infrastructure. Alpha has 10+ years of experience training IT professionals.',
                'email': 'alpha@interlinkglobal.edu',
                'expertise': ['Networking', 'System Administration', 'IT Security'],
                'order': 2,
                'image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80'
            },
            {
                'name': 'Mr. Amadou Manneh',
                'position': 'Lead Design Instructor',
                'bio': 'Award-winning designer with expertise in Adobe Creative Suite. Amadou has worked with major brands across Africa.',
                'email': 'amadou@interlinkglobal.edu',
                'expertise': ['Graphic Design', 'UI/UX', 'Branding'],
                'order': 3,
                'image': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80'
            },
            {
                'name': 'Mr. Musa Jallow',
                'position': 'Programming Instructor',
                'bio': 'Full-stack developer passionate about teaching coding. Musa has built applications for fintech and e-commerce companies.',
                'email': 'musa@interlinkglobal.edu',
                'expertise': ['Web Development', 'Python', 'JavaScript'],
                'order': 4,
                'image': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80'
            },
            {
                'name': 'Mr. Lamin Sillah',
                'position': 'IT Support Specialist',
                'bio': 'Hardware expert with 8 years of hands-on experience. Lamin ensures our labs are always running smoothly.',
                'email': 'lamin@interlinkglobal.edu',
                'expertise': ['Hardware', 'System Admin', 'Troubleshooting'],
                'order': 5,
                'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80'
            },
            {
                'name': 'Mr. Omar Ceesay',
                'position': 'Cybersecurity Instructor',
                'bio': 'Certified ethical hacker training the next security experts. Omar has worked with government agencies on security initiatives.',
                'email': 'omar@interlinkglobal.edu',
                'expertise': ['Security', 'Ethical Hacking', 'Data Protection'],
                'order': 6,
                'image': 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80'
            }
        ]
        
        for member_data in team_data:
            image_file = BaseSeeder.download_image(member_data['image'])
            
            member = TeamMember.objects.create(
                name=member_data['name'],
                position=member_data['position'],
                bio=member_data['bio'],
                email=member_data['email'],
                expertise=member_data['expertise'],
                order=member_data['order'],
                is_active=True
            )
            
            if image_file:
                member.image.save(f"{member.name.lower().replace(' ', '_')}.jpg", image_file, save=True)
            
            BaseSeeder.print_success(f"Created team member: {member.name}")
        
        BaseSeeder.print_success(f"✅ Team seeding completed! Created {len(team_data)} team members")