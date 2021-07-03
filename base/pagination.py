from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class ProductSetPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 2


class YourPagination(pagination.PageNumberPagination):
    page_size = 4
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page': self.page.number,
            'results': data
        })
