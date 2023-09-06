import random
from django.db import transaction

from .models import User, Address, Certifications, Profession
from faker import Faker

fake = Faker()


@transaction.atomic
def create_dummy_data(num_entries):
    # Create 10,000 users
    for _ in range(10000):
        with transaction.atomic():
            user = User.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone=fake.random_int(min=600000000, max=999999999),
            )

            # Create Address for each user
            Address.objects.create(
                user=user,
                local_address=fake.street_address(),
                city=fake.city(),
            )

            # Create Profession for each user
            Profession.objects.create(
                user=user,
                profession=fake.job(),
            )

            # Create Certifications for each user
            for _ in range(
                random.randint(1, 5)
            ):  # Random number of certifications (1 to 5)
                Certifications.objects.create(
                    user=user,
                    certificate_name=fake.word(),
                    duration=random.randint(1, 12),  # Random duration (1 to 12 months)
                )


if __name__ == "__main__":
    create_dummy_data(10000)
