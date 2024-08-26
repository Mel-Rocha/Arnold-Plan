from rest_framework import status
from django.db import IntegrityError
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework.viewsets import mixins, GenericViewSet


code = {
    200: status.HTTP_200_OK,
    201: status.HTTP_201_CREATED,
    202: status.HTTP_202_ACCEPTED,
    204: status.HTTP_204_NO_CONTENT,
    206: status.HTTP_206_PARTIAL_CONTENT,
    400: status.HTTP_400_BAD_REQUEST,
    401: status.HTTP_401_UNAUTHORIZED,
    402: status.HTTP_402_PAYMENT_REQUIRED,
    403: status.HTTP_403_FORBIDDEN,
    404: status.HTTP_404_NOT_FOUND,
    405: status.HTTP_405_METHOD_NOT_ALLOWED,
    406: status.HTTP_406_NOT_ACCEPTABLE,
    408: status.HTTP_408_REQUEST_TIMEOUT,
    500: status.HTTP_500_INTERNAL_SERVER_ERROR
}

message_code = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No content",
    206: "Partial content",
    400: "Bad request",
    401: "Unauthorized",
    402: "Payment required",
    403: "Forbidden",
    404: "Not found",
    405: "Method not allowed",
    406: "Not acceptable",
    408: "Request timeout",
    500: "Internal server error",
}


def response_log_user(request, content, status_code=200):
    user = None

    if not isinstance(request.user, AnonymousUser):
        user = {
            'id': request.user.id,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
            'is_active': request.user.is_active,
            'is_nutritionist': request.user.is_nutritionist,
            'is_athlete': request.user.is_athlete,
        }

    return Response(data={"user": user, "content": content}, status=status_code)


class List(GenericViewSet, mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return response_log_user(request, self.get_paginated_response(serializer.data).data)
            serializer = self.get_serializer(queryset, many=True)
            return response_log_user(request, serializer.data)
        except Exception as e:
            return response_log_user(request, str(e), 400)


class Create(GenericViewSet, mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return response_log_user(request, serializer.data, 201)
        except IntegrityError:
            return response_log_user(request, "Integrity error.", 409)
        except Exception as e:
            return response_log_user(request, str(e), 400)


class Retrieve(GenericViewSet, mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response_log_user(request, serializer.data)
        except Exception as e:
            return response_log_user(request, str(e), 400)


class Update(GenericViewSet, mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return response_log_user(request, serializer.data)
        except Exception as e:
            return response_log_user(request, str(e), 400)


class Destroy(GenericViewSet, mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save()
            return response_log_user(request, True, 204)
        except Exception as e:
            return response_log_user(request, str(e), 400)
