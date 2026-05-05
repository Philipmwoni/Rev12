import random
import string


def generate_activation_code():
    """Generate a random 6-digit activation code."""
    return ''.join(random.choices(string.digits, k=6))