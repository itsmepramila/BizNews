from biznews.models import Post, Category, Tag

def navigation(request):
    categories=Category.objects.all()
    tags=Tag.objects.all()
    featured_posts = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[:9]
    
    tranding_posts = Post.objects.filter(
            status="active", published_at__isnull=False
        )[:9]
    featured_post = (
            Post.objects.filter(status="active", published_at__isnull=False)
            .order_by("-views_count")
            .first()
        )
    
    
    return{
        "categories":categories,
        "tags":tags,
        "featured_posts":featured_posts,
        "tranding_posts":tranding_posts,
        "featured_post":featured_post,
    }
     