from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )



class PhotoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class PhotoPageNumberPagination(PageNumberPagination):
    page_size = 5