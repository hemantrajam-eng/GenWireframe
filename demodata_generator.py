import random
from datetime import datetime, timedelta


def generate_sample_value(field_type, field_name):

    name = (field_name or "").lower()

    if "case" in name and "number" in name:
        return random.randint(7000000,7999999)

    if "cif" in name:
        return random.randint(10000000,99999999)

    if "loan" in name and "number" in name:
        return random.randint(1000,9999)

    if "account" in name:
        return random.randint(100000000000,999999999999)

    if "customer" in name or "name" in name:
        return random.choice([
            "Rahul Sharma",
            "Amit Patel",
            "Priya Nair",
            "Neha Verma",
            "Parth Kapoor"
        ])

    if "owner" in name or "assigned" in name:
        return random.choice([
            "Operations Team",
            "Customer Support",
            "Branch Manager",
            "Loan Processing Team"
        ])

    if "email" in name:
        return "customer@gmail.com"

    if "phone" in name:
        return "+91 9876543210"

    if "amount" in name:
        return f"{random.randint(1000,500000):,}"

    if "date" in name:
        date = datetime.now() - timedelta(days=random.randint(1,400))
        return date.strftime("%d-%b-%Y")

    return ""