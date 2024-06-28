# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = itemAdapter(item)
        field_names = adapter.field_names()

        #strip strings to remove whitespaces
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
        
        #lowercase category and product_type strings
        lowercase_keys = ['category', 'product_type']
        for field_name in lowercase_keys:
            value = adapter.get(field_name)
            adapter[field_name] = value.lower()
        
        #remove £ sign and convert string to float
        price_keys = ['price', 'tax', 'price_excl_tax', 'price_incl_tax']
        for field_name in price_keys:
            value = adapter.get(field_name)
            value = value.replace('£', '')
            adapter[field_name] = float(value)
        
        #extract number of books in stock
        availability_str = adapter.get('availability')
        availability_list = availability_str.split('(')
        if len(availability_list) < 2:
            adapter['availability'] = 0
        else:
            adapter['availability'] = int(availability_list[1].split(' '))

        #convert number of reviews to string
        adapter['num_reviews'] = int(adapter.get('num_reviews'))

        #convert stars text to number
        stars = adapater.get('stars').split(' ')[1].lower()
        stars_dict = {'zero':0, 'one':1, 'two':2, 'three':3, 'four':4} 
        adapter['stars'] = stars_dict[stars]

        return item
