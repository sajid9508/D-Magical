from django.core.management.base import BaseCommand
from salon.models import Service

class Command(BaseCommand):
    help = "Seeds the database with standard salon services for 'D' MAGICAL Family Salon"

    def handle(self, *args, **options):
        services_data = [
            # Hair Grooming & Styling
            {
                'name': 'Classic Haircut',
                'category': 'HAIR',
                'description': 'Professional haircut tailored to your face shape, including a quick hair rinse and style.',
                'price': 100.00,
                'duration_minutes': 30,
                'image_url': 'https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=500&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'name': 'Premium Hair Styling & Wash',
                'category': 'HAIR',
                'description': 'Deep cleaning shampoo, nourishing conditioner, advanced haircut, and signature styling with premium products.',
                'price': 450.00,
                'duration_minutes': 45,
                'image_url': 'https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=500&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'name': 'Global Hair Coloring',
                'category': 'HAIR',
                'description': 'Full-head hair coloring using premium, ammonia-free professional colors for a rich, vibrant look.',
                'price': 1800.00,
                'duration_minutes': 90,
                'image_url': 'https://images.unsplash.com/photo-1562322140-8baeececf3df?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
            {
                'name': 'Classic Shave & Beard Trim',
                'category': 'HAIR',
                'description': 'Precise beard grooming, classic close shave, sharp line-ups, and hot towel styling.',
                'price': 50.00,
                'duration_minutes': 20,
                'image_url': 'https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },

            # Skin Care & Facials
            {
                'name': 'O3+ Bridal Glow Facial',
                'category': 'SKIN',
                'description': 'Premium skin brightening and deep cleansing facial therapy designed for weddings and special occasions.',
                'price': 2500.00,
                'duration_minutes': 60,
                'image_url': 'https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?w=500&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'name': 'De-Tan Therapy',
                'category': 'SKIN',
                'description': 'Highly effective tan removal and skin soothing mask for face and neck.',
                'price': 400.00,
                'duration_minutes': 30,
                'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
            {
                'name': 'Charcoal Deep Cleanse Mask',
                'category': 'SKIN',
                'description': 'Purifying charcoal peel-off mask to remove blackheads, extract deep impurities, and control excess oil.',
                'price': 500.00,
                'duration_minutes': 40,
                'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },

            # Spa & Body
            {
                'name': 'Stress Relief Head Massage',
                'category': 'SPA',
                'description': 'Deeply relaxing hot oil head massage focusing on pressure points to melt away stress.',
                'price': 350.00,
                'duration_minutes': 30,
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
            {
                'name': 'Full Body Deep Tissue Spa',
                'category': 'SPA',
                'description': 'Therapeutic full-body massage using premium aromatherapy oils, followed by a hot towel steam.',
                'price': 2200.00,
                'duration_minutes': 60,
                'image_url': 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=500&auto=format&fit=crop&q=80',
                'is_featured': True,
            },

            # Bridal / Groom
            {
                'name': 'Magical Bridal Makeup & Hair',
                'category': 'MAKEUP',
                'description': 'Elite HD makeup, hair design, saree/lehenga draping, and jewelry setting by senior stylists.',
                'price': 7500.00,
                'duration_minutes': 150,
                'image_url': 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=500&auto=format&fit=crop&q=80',
                'is_featured': True,
            },
            {
                'name': 'Elite Groom Styling Package',
                'category': 'MAKEUP',
                'description': 'Complete grooming package: premium haircut, shave, de-tan, express facial, and wedding day hair styling.',
                'price': 4500.00,
                'duration_minutes': 120,
                'image_url': 'https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },

            # Nail Art & Care
            {
                'name': 'Premium Gel Pedicure',
                'category': 'NAILS',
                'description': 'Exfoliating sea salt scrub, relaxing foot massage, cuticle care, and long-lasting professional gel polish.',
                'price': 800.00,
                'duration_minutes': 45,
                'image_url': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
            {
                'name': 'Classic Manicure',
                'category': 'NAILS',
                'description': 'Nourishing hand massage, nail shaping, cuticle therapy, and protective clear or color coating.',
                'price': 500.00,
                'duration_minutes': 30,
                'image_url': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=500&auto=format&fit=crop&q=80',
                'is_featured': False,
            },
        ]

        created_count = 0
        updated_count = 0
        for s in services_data:
            obj, created = Service.objects.update_or_create(
                name=s['name'],
                category=s['category'],
                defaults={
                    'description': s['description'],
                    'price': s['price'],
                    'duration_minutes': s['duration_minutes'],
                    'image_url': s['image_url'],
                    'is_featured': s['is_featured']
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded database! Created {created_count} and updated {updated_count} services."))

        # Seed default owner user
        from django.contrib.auth.models import User
        from salon.models import UserProfile
        
        owner_username = 'owner'
        owner_email = 'owner@dmagicalsalon.com'
        owner_phone = '9740637692'
        owner_password = 'magicalpassword123'
        
        user, user_created = User.objects.get_or_create(
            username=owner_username,
            defaults={
                'email': owner_email,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if user_created or not user.check_password(owner_password):
            user.set_password(owner_password)
            user.save()
            
        # Ensure profile exists
        UserProfile.objects.update_or_create(
            user=user,
            defaults={'phone_number': owner_phone}
        )
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded default owner: Email: {owner_email} | Phone: {owner_phone} | Password: {owner_password}"))
