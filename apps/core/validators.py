from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_not_in_future(value):
    """
    Validador que verifica se uma data não está no futuro.
    """
    if value > timezone.now().date():
        raise ValidationError("Datas futuras não são permitidas.")
