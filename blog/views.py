from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Blog, BlogCategory
from .forms import BlogForm, BlogCategoryForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class BlogListView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-upload_date']

    def test_func(self):
        return self.request.user.is_staff_user() or self.request.user.is_admin()

class BlogDetailView(LoginRequiredMixin, UserPassesTestMixin,DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'

    def test_func(self):
        return self.request.user.is_staff_user() or self.request.user.is_admin()

class BlogCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff_user() or self.request.user.is_admin()

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author or self.request.user.is_staff or self.request.user.is_admin()

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author or self.request.user.is_staff_user() or self.request.user.is_admin()


class BlogCategoryListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = BlogCategory
    template_name = 'blogs/category_list.html'
    context_object_name = 'categories'
    ordering = ['-created_at']

    def test_func(self):
        return self.request.user.is_staff_user() or self.request.user.is_admin()

class BlogCategoryCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = BlogCategory
    form_class = BlogCategoryForm
    template_name = 'blogs/category_form.html'
    success_url = reverse_lazy('blog_category_list')

    def test_func(self):
        return self.request.user.is_staff_user() or self.request.user.is_admin()

class BlogCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogCategory
    form_class = BlogCategoryForm
    template_name = 'blogs/category_form.html'
    success_url = reverse_lazy('blog_category_list')

    def test_func(self):
        return self.request.user.is_staff_user() or self.request.user.is_admin()

class BlogCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogCategory
    success_url = reverse_lazy('blog_category_list')

    def test_func(self):
        return self.request.user.is_staff_user() or self.request.user.is_admin()

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Periksa jika permintaan adalah AJAX
            category = get_object_or_404(BlogCategory, pk=self.kwargs['pk'])
            category.delete()
            return JsonResponse({'success': True, 'message': 'Category deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
