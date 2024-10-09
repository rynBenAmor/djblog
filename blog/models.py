from django.conf import settings
from django.db import models
from django.utils import timezone

from django.utils.text import slugify


#custom manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)  



class Post(models.Model):

    #status choices
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date='publish', blank=True, max_length=250)#now the title can be unique to publish date
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts' )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT )

    
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title
    

    #auto uniquely slugify the title
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the initial slug
            base_slug = slugify(self.title)
            slug = base_slug
            """
            counter = 1

            # Check if the slug already exists in the database
            while Post.objects.filter(slug=slug).exists():
                # If it exists, append a counter to make the slug unique
                slug = f'{base_slug}-{counter}'
                counter += 1
            """

            self.slug = slug

        super().save(*args, **kwargs)


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:detail', args=[
                                                self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug,
                                        ]
                    )