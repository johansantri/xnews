from django.contrib import admin
from .models import Partners, Category
from django.contrib.auth.models import User


admin.site.register(Category)
@admin.register(Partners)
class Blog(admin.ModelAdmin):
    list_display = ('partner_name', 'slug', 'pic', 'publish', 'status','category')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('partner_name', 'descriptions')
    prepopulated_fields = {'slug': ('partner_name',)}
   # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "pic":
            kwargs["queryset"] = User.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

