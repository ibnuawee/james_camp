from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import AboutContent
from .forms import AboutContentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class AboutContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AboutContent
    form_class = AboutContentForm
    template_name = 'content/about_content_form.html'
    success_url = reverse_lazy('content_admin')

    def get_object(self, queryset=None):
        obj, created = AboutContent.objects.get_or_create(
            defaults={
                "address": "Sekaran, Gunungpati, Semarang",
                "phone": "+62 81217886415",
                "email": "jamescamp@gmail.com",
                "heading": "Welcome to JamesCamp",
                "description": (
                    "Kami adalah penyedia alat camping terpercaya yang berdedikasi untuk menghadirkan pengalaman alam terbuka yang tak terlupakan. "
                    "Didirikan dengan semangat cinta petualangan, James Camp memahami bahwa kualitas peralatan dapat membuat perbedaan besar dalam setiap perjalanan outdoor Anda."
                ),
                "link_text": "Search Vehicle",
                "link_url": "#",
            }
        )
        return obj

    def test_func(self):
        return self.request.user.is_admin()
