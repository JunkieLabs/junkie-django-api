from django.db import models

# Create your models here.
from django.db import models as basemodels

# Create your models here.
from pynamodb import models
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute, JSONAttribute
from ..env import DB_HOST, DB_REGION
'''
id : unique identifier
category : eg. app, illustation, design etc
name : "product's name"
detail : ["blogging","dummy app"]
attr : {platform:[android, web, ], type:{clone }, language:[kotlin, python, ]}
notes : ["Material design", "QR Scanner", "Jetpack"]
'''

class Products(models.Model):
    
    class Meta:
        table_name = "products-table"
        host = DB_HOST
        region = DB_REGION
        read_capacity_units=5
        write_capacity_units=5
    
    id = UnicodeAttribute(range_key=True, null=False)
    category = UnicodeAttribute(hash_key=True, null=False)
    name = UnicodeAttribute(null=False)
    detail = UnicodeAttribute(null=False)
    notes = ListAttribute(null=False)
    attributes = ListAttribute(null=False)
    status = UnicodeAttribute(null=False, default='restricted')
    cns = ListAttribute(null=False)
    # template = MapAttribute(default={})
    template = JSONAttribute()