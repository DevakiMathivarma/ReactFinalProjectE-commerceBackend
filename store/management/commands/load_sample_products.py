from django.core.management.base import BaseCommand
from store.models import Product

SAMPLES = [
    {
        "name": "Puma Crocs Brown",
        "price": 499.00,
        "external_image": "https://images.unsplash.com/photo-1585386959984-a415522f1b6b?auto=format&fit=crop&w=800&q=80",
    },
    {
        "name": "Puma Becket Orange",
        "price": 799.00,
        "external_image": "https://images.unsplash.com/photo-1519744792095-2f2205e87b6f?auto=format&fit=crop&w=800&q=80",
    },
    {
        "name": "Lunar Flip Flop Black",
        "price": 299.00,
        "external_image": "https://images.unsplash.com/photo-1526178612466-3f9b08f84f3f?auto=format&fit=crop&w=800&q=80",
    },
    {
        "name": "Regatta Trainers Grey",
        "price": 1299.00,
        "external_image": "https://images.unsplash.com/photo-1520975698515-8b7e8c1d7b7d?auto=format&fit=crop&w=800&q=80",
    },
]

class Command(BaseCommand):
    help = "Load sample products with external images"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        for s in SAMPLES:
            Product.objects.create(
                name=s["name"],
                price=s["price"],
                external_image=s["external_image"],
                stock=10,
            )
        self.stdout.write(self.style.SUCCESS("Sample products created"))
