from django.db import models

class SiteInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name='Site Name')
    about = models.TextField(blank=True, null=True, verbose_name='About')
    image_header = models.ImageField(upload_to='header/%Y/%m/%d', blank=True, null=True, verbose_name='Header Image')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name='Email Address')
    address = models.TextField(blank=True, null=True, verbose_name='Address')
    instagram = models.URLField(blank=True, null=True, verbose_name='Instagram URL')
    telegram = models.URLField(blank=True, null=True, verbose_name='Telegram URL')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Site Information'
        verbose_name_plural = 'Site Information'

    def __str__(self):
        return self.name if self.name else "Site Info"

    @classmethod
    def get_info(cls):
        # Always return the latest SiteInfo instance, or None if not exists
        return cls.objects.order_by('-created_at').first()