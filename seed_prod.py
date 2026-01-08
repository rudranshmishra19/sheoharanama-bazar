import os
import django
import random
from faker import Faker
from django.utils.text import slugify

# 1. Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from store.models import Product, Category

def seed_database():
    fake = Faker()
    print(" Starting database seeding with your categories...")

    # 2. Create Your Specific Categories
    categories = ['Snacks', 'Clothing', 'Pickles']
    category_objs = []
    
    for cat_name in categories:
        # get_or_create ensures we don't make duplicates
        cat, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name)}
        )
        category_objs.append(cat) # This was missing in your version!
    
    print(f"Created/Verified {len(category_objs)} categories: {categories}")

    # 3. Create 50 Products
    print(" Generating 50 products...")
    for _ in range(50):
        product_name = fake.catch_phrase()
        Product.objects.create(
            name=product_name,
            slug=slugify(product_name) + "-" + str(random.randint(1000, 9999)), # Unique slug
            description=fake.paragraph(nb_sentences=3),
            price=round(random.uniform(10.0, 500.0), 2),
            category=random.choice(category_objs), # Now category_objs has data
            stock=random.randint(1, 100),
            available=True
        )

    print(" Success! 50 products have been added to your database.")

if __name__ == "__main__":
    seed_database()