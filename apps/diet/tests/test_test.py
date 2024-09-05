# import pytest
# from rest_framework.test import APIClient
# from django.urls import reverse
# from rest_framework import status
#
#
# @pytest.mark.django_db
# def test_api_get_items():
#     client = APIClient()
#     url = reverse('token_obtain_pair')  # substitua pelo nome da sua rota
#     response = client.post(url)
#
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) > 0
