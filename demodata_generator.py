from faker import Faker
import random

fake = Faker("en_IN")


def generate_sample_value(field_type, field_name):

    if not field_name:
        return ""

    name = str(field_name).lower()

    try:

        # Name fields
        if "name" in name:
            return fake.name()

        # CIF / Account
        if "cif" in name or "account" in name:
            return random.randint(10000000, 99999999)

        # Email
        if "email" in name:
            return fake.email()

        # Phone
        if "phone" in name or "mobile" in name:
            return fake.phone_number()

        # Address
        if "address" in name:
            return fake.address()

        # City
        if "city" in name:
            return fake.city()

        # Country
        if "country" in name:
            return fake.country()

        # Company
        if "company" in name:
            return fake.company()

        # URL
        if "url" in name:
            return fake.url()

        # Date fields
        if field_type in ["Date", "DateTime"]:
            return fake.date()

        # Amount
        if field_type in ["Amount", "Decimal", "Currency"]:
            return round(random.uniform(1000, 500000), 2)

        # Number
        if field_type in ["Number", "BigInt"]:
            return random.randint(1, 100)

        # Percentage
        if field_type == "Percentage":
            return random.randint(1, 100)

        # Text
        if field_type in ["Text", "LongText", "Comments"]:
            return fake.word()

        # Default fallback
        return ""

    except:
        return ""
