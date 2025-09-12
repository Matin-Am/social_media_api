from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Post,Relation
from django.core.cache import cache

@receiver([post_save,post_delete],sender=Post)
def invalidate_product_cache(sender,**kwargs):
    """
    invalidate Post list caches when a Post is created or deleted. 
    """
    cache.delete_pattern("*list_posts*")


@receiver(signal=[post_delete,post_save],sender=Relation)
def invalidate_user_relations_cache(sender,**kwargs):
    """
    invalidate all User s' list relations cache when a relation created or deleted 
    """
    cache.delete_pattern("*list_relations*")