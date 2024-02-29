from django.shortcuts import render
from .models import Post, Comment
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count 
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

def post_list(request, tag_slug=None):


    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {'posts':posts, 'tag':tag}
    return render(request, 'blog/post/list.html', context)

def post_detail(request,year, month, day, post):

    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # List of similar posts
    post_tag_ids  = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids.exclude(id=post.id))
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {'post':post, 'similar_posts':similar_posts}
    return render(request, 'blog/post/detail.html',context )

@require_POST
def comment_post(request):

    post_id = request.POST.get('post_id')
    email = request.POST.get('email')
    body = request.POST.get('body')
    name = request.POST.get('name')
    #Get the post
    post = get_object_or_404(Post, id=post_id)

    if name:
        comment = Comment(post=post, name=name, email=email, body=body)
        comment.save()
        context = render_to_string('async/blog/comment.html', {'post':post})
        
        return JsonResponse({'data':context})
    return JsonResponse({'data':'error'})