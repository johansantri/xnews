from django.contrib import admin
from .models import Post, Comment, Category
from django.contrib.auth.models import User


admin.site.register(Category)
@admin.register(Post)
class Blog(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status','category')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
   # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display=('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')