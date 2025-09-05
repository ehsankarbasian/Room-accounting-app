from django.core.paginator import Paginator


class PaginationMixin:
    
    def get_paginated_items(self, request, query_set):
        page_number = request.GET.get('page', 1)
        paginator = Paginator(query_set, self.page_size)
        page_obj = paginator.get_page(page_number)
        
        return page_obj
