from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import no_body, swagger_auto_schema
from django.core.paginator import Paginator
from django.db.models import Count, Q

from standard.response import ErrorMessage, MessageCode, get_error_response


from .models import User
from .serializer import CertificationsModelSerializer


class UserMultiView(APIView):
    permission_classes = [AllowAny]

    class UserGetSerializer(serializers.Serializer):
        page = serializers.IntegerField(required=False, default=1)
        limit = serializers.IntegerField(
            required=False, default=10, min_value=10, max_value=100000
        )

        search_query = serializers.CharField(required=False)
        order_by = serializers.CharField(required=False)
        filter_query = serializers.CharField(required=False)

    class UserModelSerializer(serializers.ModelSerializer):
        local_address = serializers.SerializerMethodField()
        number_of_certification = serializers.SerializerMethodField()
        list_cirtificates = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = [
                "id",
                "name",
                "email",
                "phone",
                "local_address",
                "number_of_certification",
                "list_cirtificates",
            ]

        def get_local_address(self, user_obj):
            return user_obj.addresses.local_address

        def get_number_of_certification(self, user_obj):
            return user_obj.number_of_certification

        def get_list_cirtificates(self, user_obj):
            return CertificationsModelSerializer(
                user_obj.certifications, many=True
            ).data

    @swagger_auto_schema(
        query_serializer=UserGetSerializer,
        request_body=no_body,
        responses={200: UserModelSerializer},
    )
    def get(self, *args, **kwargs):
        user_get_serializer = self.UserGetSerializer(data=self.request.GET)
        if not user_get_serializer.is_valid():
            return Response(
                user_get_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        page = user_get_serializer.validated_data.get("page")
        limit = user_get_serializer.validated_data.get("limit")
        search_query = user_get_serializer.validated_data.get("search_query")
        order_by = user_get_serializer.validated_data.get("order_by")
        filter_query = user_get_serializer.validated_data.get("filter_query")
        
        q_obj_base = Q()

        # filter
        if filter_query:
            q_obj_filter = Q()
            if filter_query == "equal_5":
                q_obj_filter |= Q(number_of_certification=5)
            elif filter_query == "below_5":
                q_obj_filter |= Q(number_of_certification__lt=5)
            elif filter_query == "equal_4":
                q_obj_filter |= Q(number_of_certification=4)
            elif filter_query == "equal_3":
                q_obj_filter |= Q(number_of_certification=3)
            elif filter_query == "equal_2":
                q_obj_filter |= Q(number_of_certification=2)
            elif filter_query == "equal_1":
                q_obj_filter |= Q(number_of_certification=1)

            q_obj_base &= q_obj_filter


        # search
        if search_query:
            q_obj_search = Q()
            q_obj_search |= Q(name__icontains=search_query)  # search by name
            q_obj_search |= Q(email__icontains=search_query)  # search by email

            q_obj_base &= q_obj_search

        # sort
        if order_by:
            order_by = order_by
        else:
            order_by = "-id"

        user_objs =User.objects.prefetch_related("addresses", "certifications").annotate(number_of_certification=Count("certifications")).filter(q_obj_base).order_by(order_by)
        
        if page is not None and limit is not None:
            paginator = Paginator(user_objs, limit)
            page_obj = paginator.get_page(page)
            result = page_obj.object_list
            count = paginator.count
        else:
            result = user_objs
            count = len(result)

        response_data = {
            "size": len(result),
            "data": self.UserModelSerializer(
                result,
                many=True,
            ).data,
            "count": count,
        }
        return Response(response_data, status=status.HTTP_200_OK)
