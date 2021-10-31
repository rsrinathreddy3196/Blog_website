from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Post
from django.views import View
from .forms import commentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.


class MainPageView(ListView):
    template_name = "blog/main_page.html"
    model = Post
    context_object_name = "posts"
    ordering = ["date"]

    def get_queryset(self):
        queryset= super().get_queryset()
        data = queryset[0:]
        return data

# alternative for main_page........................................................
# def main_page(request):
#     latest_posts= Post.objects.all().order_by("date")[0:]
#     return render(request, "blog/main_page.html",{

#       "posts":latest_posts

#     })
# ......................................................................... 

#  here we are not adding qureyset because we dont want to limit the number of posts //
class PostsView(ListView):
  template_name  ="blog/all-posts.html"
  model = Post
  context_object_name = "all_Posts"
  ordering = ["date"]

# alternative for all_posts....................................
# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request,"blog/all-posts.html",{

#         "all_Posts":all_posts
#     })
# ...............................................................

class IndividualPageView(View):

  def is_stored_post(self, request, post_id):
        stored_post = request.session.get("stored_post")
        if stored_post is not None:
          is_saved_for_later = post_id in stored_post
        else:
          is_saved_for_later = False

        return is_saved_for_later
 
  def get(self, request,slug):
     post = Post.objects.get(slug=slug)
     context={
          "post":post,
          "post_tags" :post.tags.all(),
          "comment_form": commentForm(),
          "comments": post.comments.all().order_by("-id"),
          "saved_for_later": self.is_stored_post(request, post.id)

     }
     return render(request, "blog/post_detail.html", context)


  def post(self,request,slug): 
      comment_form = commentForm(request.POST)
      post = Post.objects.get(slug=slug)
      
      
      if comment_form.is_valid():
          comment= comment_form.save(commit=False)
          comment.post = post
          comment.save()
          return HttpResponseRedirect(reverse("individual_page", args=[slug]))


      context={
          "post":post,
          "post_tags" :post.tags.all(),
          "comment_form": comment_form,
          "comments": post.comments.all().order_by("-id"),
          "saved_for_later": self.is_stored_post(request, post.id)

     } 
      return render(request, "blog/post_detail.html", context)

  # def get_context_data(self, **kwargs):
  #     context = super().get_context_data(**kwargs)
  #     context["post_tags"] = self.object.tags.all()
  #     context["comment_form"] = commentForm()
  #     return context

# alternative for post detail page.............................................
# def individual_page(request,slug):
#    identified_post = Post.objects.get(slug=slug)
#    return render(request,"blog/post_detail.html",{

#      "post":identified_post,
#      "post_tags":identified_post.tags.all()
#    })


class ReadMeLateView(View):
  def get(self,request):
    stored_post  = request.session.get("stored_post")

    context={}
    if stored_post is None or len(stored_post)==0:
      context["posts"]=[]
      context["has_posts"] = False

    else:
      posts = Post.objects.filter(id__in=stored_post)
      context["posts"] = posts
      context["has_post"]  = True

    return render(request, "blog/stored_post.html", context)  



  def post(self, request):
    stored_post  = request.session.get("stored_post")

    if stored_post is None:
      stored_post =[]

    post_id = int(request.POST["post_id"])

    if post_id not in stored_post:
      stored_post.append(post_id)
    else:
        stored_post.remove(post_id)  
    
    request.session["stored_post"] = stored_post  

    return HttpResponseRedirect("/")  