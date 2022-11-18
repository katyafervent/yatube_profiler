import time
from functools import lru_cache

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from posts.decorators import admin_field, show_time
from posts.models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    autocomplete_fields = ('group', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_per_page = 1000

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs: QuerySet = super().get_queryset(request)
        # qs = qs.select_related('author', 'group')
        qs = qs.prefetch_related('author', 'group')
        # print(qs.query)

        return qs

    @show_time
    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = (
        'pk',
        'title',
        'slug',
        'some_calculations'
    )
    search_fields = ('title',)

    @admin_field(short_description='Сложное вычисление')
    @lru_cache()
    def some_calculations(self, obj: Group) -> str:
        time.sleep(0.1)
        return f'result={obj.pk}'

    # @show_time
    # def changelist_view(self, request, extra_context=None):
    #     return super().changelist_view(request, extra_context)


admin.site.register(Comment)
admin.site.register(Follow)
