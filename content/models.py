from django.db import models


class AboutContent(models.Model):
    address = models.TextField("Address", default="Sekaran, Gunungpati, Semarang")
    phone = models.CharField("Phone", max_length=20, default="+62 81217886415")
    email = models.EmailField("Email", default="jamescamp@gmail.com")
    heading = models.CharField("Heading", max_length=200, default="Welcome to Jamescamp")
    description = models.TextField("Description", default=(
        "Kami adalah penyedia alat camping terpercaya yang berdedikasi untuk menghadirkan pengalaman alam terbuka yang tak terlupakan. Didirikan dengan semangat cinta petualangan, James Camp memahami bahwa kualitas peralatan dapat membuat perbedaan besar dalam setiap perjalanan outdoor Anda."
    ))
    link_text = models.CharField("Button Text", max_length=100, default="Search Item")
    link_url = models.URLField("Button URL", default="#")

    def __str__(self):
        return "About Content"

