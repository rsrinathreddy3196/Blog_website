from django.contrib import admin
from . models import Tag, Author, Post,comment

# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display = ("title", "date",)
    list_filter = ("author", "title", "date",)
    prepopulated_fields = {"slug":("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name","post")    

admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Post, postAdmin)
admin.site.register(comment,CommentAdmin)



