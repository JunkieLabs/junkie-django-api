#from django.db import models

from pynamodb import models
from pynamodb.attributes import UnicodeAttribute

from junkie_django_api.env import DB_HOST, DB_REGION
#from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, IncludeProjection

'''
id : productionLine id
actionValue : Low/Mid/High if priority else 0/1 if vote
actionIp  : ip addresses & action type (0:0:0:0_vote)

'''

class ProductionLineAction(models.Model):
    
    class Meta:
        table_name = "productionLineAction-table"
        host = DB_HOST
        region = DB_REGION
        read_capacity_units=5
        write_capacity_units=5
    
    pId = UnicodeAttribute(hash_key=True, null=False)
    ipAction = UnicodeAttribute(range_key=True, null=False)
    actionVal = UnicodeAttribute()
    # id = UnicodeAttribute()
