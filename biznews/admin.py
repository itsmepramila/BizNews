from django.contrib import admin
from biznews.models import Post, Category, Tag, Contact

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Contact)


from django_summernote.admin import SummernoteModelAdmin
from .models import Post

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)

