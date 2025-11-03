import pandas as pd
import os
import django
import sys
from django.utils.text import slugify
from django.db import transaction, IntegrityError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Django environment
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from store.models import Product, Category

def import_csv_data(csv_file_path='store/data/ecommerce_products.csv'):
    """
    Import CSV data into Django models with proper error handling and bulk operations
    """
    try:
        # Read CSV with error handling
        df = pd.read_csv(csv_file_path)
        logger.info(f"Successfully loaded CSV with {len(df)} rows")
        
    except FileNotFoundError:
        logger.error(f"CSV file not found at {csv_file_path}")
        return
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return

    # Data validation and cleaning
    required_columns = ['Category', 'Product', 'Price', 'Stock']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        return

    # Clean data
    df = df.dropna(subset=required_columns)  # Remove rows with missing required data
    df['Category'] = df['Category'].str.strip().str.title()
    df['Product'] = df['Product'].str.strip()
    
    # Use transaction for data integrity
    try:
        with transaction.atomic():
            categories_created = 0
            products_created = 0
            products_updated = 0
            
            # Process categories first
            category_map = {}
            unique_categories = df['Category'].unique()
            
            for category_name in unique_categories:
                category_slug = slugify(category_name)
                category, created = Category.objects.get_or_create(
                    slug=category_slug,
                    defaults={'name': category_name}
                )
                category_map[category_name] = category
                if created:
                    categories_created += 1
                    logger.info(f"Created new category: {category_name}")
            
            # Process products
            for _, row in df.iterrows():
                category = category_map[row['Category']]
                product_name = row['Product']
                product_slug = slugify(product_name)
                
                # Use get_or_create to handle duplicates gracefully
                product, created = Product.objects.get_or_create(
                    slug=product_slug,
                    defaults={
                        'category': category,
                        'name': product_name,
                        'description': row.get('Description', ''),
                        'price': float(row['Price']),
                        'stock': int(row['Stock']),
                        'available': True
                    }
                )
                
                if created:
                    products_created += 1
                    logger.info(f"Created product: {product_name}")
                else:
                    # Update existing product if needed
                    update_fields = []
                    if product.price != float(row['Price']):
                        product.price = float(row['Price'])
                        update_fields.append('price')
                    if product.stock != int(row['Stock']):
                        product.stock = int(row['Stock'])
                        update_fields.append('stock')
                    if product.name != product_name:
                        product.name = product_name
                        update_fields.append('name')
                    
                    if update_fields:
                        product.save(update_fields=update_fields)
                        products_updated += 1
                        logger.info(f"Updated product: {product_name} - Fields: {', '.join(update_fields)}")
            
            # Summary
            logger.info(f"Import completed successfully!")
            logger.info(f"Categories created: {categories_created}")
            logger.info(f"Products created: {products_created}")
            logger.info(f"Products updated: {products_updated}")
            logger.info(f"Total categories in database: {Category.objects.count()}")
            logger.info(f"Total products in database: {Product.objects.count()}")
            
    except IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during import: {e}")

def import_csv_bulk_optimized(csv_file_path='store/data/ecommerce_products.csv'):
    """
    Alternative version using bulk operations for better performance with large datasets
    """
    try:
        df = pd.read_csv(csv_file_path)
        df = df.dropna(subset=['Category', 'Product', 'Price', 'Stock'])
        
        categories_to_create = []
        products_to_create = []
        
        # Prepare categories
        category_data = {}
        for category_name in df['Category'].unique():
            slug = slugify(category_name)
            category_data[category_name] = slug
            if not Category.objects.filter(slug=slug).exists():
                categories_to_create.append(Category(name=category_name, slug=slug))
        
        # Bulk create categories
        if categories_to_create:
            Category.objects.bulk_create(categories_to_create)
            logger.info(f"Bulk created {len(categories_to_create)} categories")
        
        # Get all categories as a mapping
        category_objs = {cat.slug: cat for cat in Category.objects.all()}
        
        # Prepare products
        existing_slugs = set(Product.objects.values_list('slug', flat=True))
        
        for _, row in df.iterrows():
            category_slug = slugify(row['Category'])
            product_slug = slugify(row['Product'])
            
            if product_slug not in existing_slugs:
                products_to_create.append(Product(
                    category=category_objs[category_slug],
                    name=row['Product'],
                    slug=product_slug,
                    description=row.get('Description', ''),
                    price=float(row['Price']),
                    stock=int(row['Stock']),
                    available=True
                ))
        
        # Bulk create products
        if products_to_create:
            Product.objects.bulk_create(products_to_create)
            logger.info(f"Bulk created {len(products_to_create)} products")
        else:
            logger.info("No new products to create")
            
    except Exception as e:
        logger.error(f"Error in bulk import: {e}")

if __name__ == "__main__":
    # Use the standard version (recommended for most cases)
    import_csv_data()
    
    # Or use bulk version for large datasets
    # import_csv_bulk_optimized()