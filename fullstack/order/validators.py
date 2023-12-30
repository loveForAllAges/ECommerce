import re
from django.core.validators import RegexValidator


def validate_phone(data):
    if re.match(r'^[87]\d{10}$', str(data)):
        return True
