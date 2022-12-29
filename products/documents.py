from django_elasticsearch_dsl import (
    Document ,
    fields,
    Index,
)
from .models import Product
PUBLISHER_INDEX = Index('elastic_demo')

PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)




@PUBLISHER_INDEX.doc_type
class ProductDocument(Document):
    
    id = fields.IntegerField(attr='id')
    fielddata=True
    name = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
    )
    desc = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
                
            }
        },
    )
   

    class Django(object):
        model = Product