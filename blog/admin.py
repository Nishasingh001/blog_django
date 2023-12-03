from django.contrib import admin
from .models import (
    PostHashTag,
    Post,
    Comment,
    Share_post
)


@admin.register(PostHashTag)
class PostHashTagadmin(admin.ModelAdmin):
    list_display=["id","hashtag"
                  
    ]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
     list_display=('id','title', 'content', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post','author', 'comment', 'created_at','email')

@admin.register(Share_post)
class Share_Post_admin(admin.ModelAdmin):
    list_display=["id","blog","token","email","date_time"
                  
    ]



