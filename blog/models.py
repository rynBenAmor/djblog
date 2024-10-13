from django.conf import settings
from django.db import models
from django.utils import timezone

from django.utils.text import slugify
from taggit.managers import TaggableManager


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

    # Creates a Many-to-Many relationship with the Tag model
    # through an intermediary model that stores Post and Tag foreign keys.
    # including automatic tag creation and manipulation by tag names.
    tags = TaggableManager()

    
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
            
            self.slug = slugify(self.title)
        #this line should always be executed regardles of if statments
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
    


#comments(many) for post(one)
class Comment(models.Model):
    post = models.ForeignKey( Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
            ordering = ['created']
            indexes = [ models.Index(fields=['created']), ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
