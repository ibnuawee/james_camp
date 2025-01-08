from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from camping.models import CampingItem, Category
from django.core.paginator import Paginator
from content.models import AboutContent
from django.views.generic import DetailView
from blog.models import Blog, BlogCategory

def is_staff_or_admin(user):
    return user.is_staff_user() or user.is_admin()

@login_required
@user_passes_test(is_staff_or_admin)
def admin_dashboard(request):
    return render(request, 'layouts/base.html')

def member_dashboard(request):
    total_items = CampingItem.objects.count()
    total_categories = Category.objects.count()
    items = CampingItem.objects.all()
    blogs = Blog.objects.all().order_by('-upload_date')[:5]
    paginator = Paginator(items, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'landingpage/home.html', {'page_obj': page_obj, 'total_items': total_items, 'total_categories': total_categories,'blogs' : blogs})

def price(request):
    items = CampingItem.objects.all()

    paginator = Paginator(items, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'landingpage/price_item.html', {'page_obj': page_obj})

def about_page(request):
    about_content = AboutContent.objects.first()
    return render(request, 'landingpage/about.html', {'about_content': about_content})

def list_blog(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'landingpage/listblog.html', {'blogs': blogs, 'page_obj': page_obj})

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'landingpage/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['recent_blogs'] = Blog.objects.exclude(pk=self.object.pk).order_by('-upload_date')[:5]
        return context
