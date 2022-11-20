import json
import logging

# from datetime import datetime

from junkie_django_api.settings import NANO_ID as _A

from nanoid import generate
from ..productionLine.models import ProductionLine
from pynamodb.expressions.operand import Path


logger = logging.getLogger(__name__)


class DynamodbProductionLine:
    if not ProductionLine.exists():
        ProductionLine.create_table(wait=True)
        logger.info("created the productionLine-table")

    def create(self, data : dict):
        product = ProductionLine()
        category = data['category']
        logger.debug(data)
        id = f"{category}_{generate(_A, 13)}"
        logger.debug("adg")
        while self.checkIdExists(id=id):
            id = f"{category}_{generate(_A, 13)}"

        # logger.debug(data.keys())
        
        try:
            product.from_json(json.dumps(data))
        except Exception as e:
            logger.exception(e)
            raise e

        # logger.debug("product :", product.attribute_values)
        product.id = id
        product.save()
        return {"id" : id}

    def delete(self, id : str):
        entity = self.getById(id=id)
        entity.delete()

    def getById(self, id : str):
        entity = ProductionLine.get(hash_key=id)
        return entity

    def getPaginationByStageQuery(self, limit : int, lastKey : str, stage : str):
        #if stage ==null then use other indexes
        productList = ProductionLine.stageIndex.query(stage, filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        return productList

    def getPaginationByQuery(self, limit : int, lastKey : str, query : str):
        #TODO
        # pass query as a filter_condition
        productList = ProductionLine.query(filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        return productList

    def getPaginationByScan(self, limit : int, lastKey : dict):
        # logger.info("dffaf")
        productList = ProductionLine.scan(filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        # logger.info("size",productList.__sizeof__())
        # logger.info("jsadhadhas")
        return productList    

    def updateSelfAttributes(self, entity : ProductionLine, data : dict):
        actions = []
        for key in data.keys():
            if (key != "id"):
                value = data.get(key)
                actions.append(Path(key).set(value))
        entity.update(actions=actions)
        return entity

    def checkIdExists(self, id : str):
        try:
            return ProductionLine.get(hash_key=id).exists()
        except Exception as e:
            logger.error(e)
            return False

