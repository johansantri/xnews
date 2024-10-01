
from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from .models import Course, Lesson


class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = [
        'public_id', 
        'updated', 
        
    ]
    extra = 0

   





@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title', 'status', 'access']
    list_filter = ['status', 'access']
    fields = ['public_id', 'title', 'description', 'status', 'image', 'access']
    readonly_fields = ['public_id']

    