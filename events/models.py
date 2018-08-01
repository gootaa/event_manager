from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db import IntegrityError


def week_hence():
    # Because default argument takes a callable
    return timezone.now() + timezone.timedelta(days=7)


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event_list_by_category', args=(self.slug,))

class Event(models.Model):
    
    host = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events')
    category = models.ForeignKey(Category, related_name='events')
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=week_hence)
    location = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    tickets_url = models.URLField(blank=True)

    class Meta:
        ordering = ('-start_time',)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        # slugify removes numbers and some letters from the title that's
        # Why we need the following loop, just in case conflicts happen because of numbers
        # getting removed from the returned slug
        unique_slug = slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
            

    def get_absolute_url(self):
        return reverse('event_detail', args=(self.slug,))

    def __str__(self):
        return self.title




