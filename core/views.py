from django.shortcuts import render

from apps.posts.models import Post

def home(request):
    return render(request, 'home.html', {
        'posts': Post.objects.filter(published=True, moderated=True, user__moderated=True, user__is_active=True)
    })
