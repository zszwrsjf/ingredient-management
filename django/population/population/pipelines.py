# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from asgiref.sync import sync_to_async

from django.db.utils import IntegrityError

from .items import IngredientItem

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


class PopulationPipeline:
    async def process_item(self, item, spider):
        """Save items yielded by spiders"""

        await self.save_to_django_db(item, spider)

        return item

    async def save_to_django_db(self, item, spider):
        """Save the given item into the DB using Django ORM"""

        try:
            await self.save_wrapper(item)
        except IntegrityError:
            return  # just return if already saved

    @sync_to_async
    def save_wrapper(self, item):
        if type(item) == IngredientItem:
            return item.instance.save_or_update_min()
        else:
            return item.save()
