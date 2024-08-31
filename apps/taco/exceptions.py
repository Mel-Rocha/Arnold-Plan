from rest_framework.exceptions import APIException


class InvalidCategoryError(APIException):
    status_code = 400  # Define o status code para 400 Bad Request
    default_detail = "Categoria inválida."  # Mensagem padrão para categoria inválida

    VALID_CATEGORIES = [
        "Cereais e derivados",
        "Verduras, hortaliças e derivados",
        "Frutas e derivados",
        "Gorduras e óleos",
        "Pescados e frutos do mar",
        "Carnes e derivados",
        "Leite e derivados",
        "Bebidas (alcoólicas e não alcoólicas)",
        "Ovos e derivados",
        "Produtos açucarados",
        "Miscelâneas",
        "Outros alimentos industrializados",
        "Alimentos preparados",
        "Leguminosas e derivados",
        "Nozes e sementes"
    ]

    def __init__(self, category):
        self.category = category
        self.detail = {
            "error": f"Categoria inválida: {category}.",
            "valid_categories": InvalidCategoryError.VALID_CATEGORIES
        }
