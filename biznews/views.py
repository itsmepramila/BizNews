from typing import Any, Dict
from django.shortcuts import render, redirect
from biznews.models import Post, Category, Tag
from django.views.generic import ListView, View, DetailView
from biznews.forms import ContactForm
from django.contrib import messages
from biznews.forms import CommentForm
from django.http import JsonResponse


# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = "bznews/main/home/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status="active", published_at__isnull=False)[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_posts"] = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[:12]
        context["latest_posts"] = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[:2]
        context["latest_posts1"] = Post.objects.filter(
        status="active", published_at__isnull=False
        ).order_by("-views_count")[2:4]
        context["latest_posts2"] = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[4:8]
        
        context["latest_posts3"] = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[8:10]
        
        context["latest_posts4"] = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[10:12]

        context["featured_post"] = (
            Post.objects.filter(status="active", published_at__isnull=False)
            .order_by("-views_count")
            .first()
        )

        context["tranding_posts"] = Post.objects.filter(
            status="active", published_at__isnull=False
        )

        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()

        return context


class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "bznews/contact.html")

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "successfulley submitted your query. we will contact you soon"
            )
            return redirect("contact")

        else:
            messages.error(
                request,
                "cannot submitted your query. please make sure all fields are valid.",
            )
            return render(
                request,
                "bznews/contact.html",
                {"form": form},
            )


class PostListView(ListView):
    model = Post
    template_name = "bznews/main/list/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        status="active", published_at__isnull=False
    ).order_by("-published_at")
    


class PostByCategoryView(ListView):
    model = Post
    template_name = "bznews/main/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            status="active",
            published_at__isnull=False,
            category=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query


class PostByTagView(ListView):
    model = Post
    template_name = "bznews/main/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            status="active",
            published_at__isnull=False,
            tag=self.kwargs["tag_id"],
        ).order_by("-published_at")
        return query


class CommentView(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post_id = request.POST["post"]
        if form.is_save():
            return redirect("post-list", post_id)
        else:
            post = Post.objects.get(id=post_id)
            return render(
                request,
                "bznews/main/list/news_detail.html",
                {"post": post, "form": form},
            )
            
class NewsletterView(View):
    def post(self, request, *args, **kwargs):
        is_ajax=request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            pass
        else:
            return JsonResponse(
                {
                    "success":False,
                    "message":"Cannot process request. Must be ab XMLHttpRequest",
                    
                },
                status=400
            )
            
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger

class PostSearchView(View):
    template_name="biznews/main/list/search.html"
    
    def get(self, request, *args, **kwargs):
        query=request.GET["query"]
        post_list=Post.objects.filter(
            (Q(title__icontains=query) | (Q(title__icontains=query))
             &(
                 Q(
                     status="active",
                     published_at__isnull=False,
                 )
             )
            )
            ).order_by('-published_at')
        
        #pagination start
        
        page=request.GET.get("page", 1)
        paginate_by=1
        paginator=Paginator(post_list, paginate_by)
        try:
            posts=paginator.page_page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)
            #pagination end
            
            
        return render(
            request,
            self.template_name,
            {"page_obj":posts, "query":query},
        )