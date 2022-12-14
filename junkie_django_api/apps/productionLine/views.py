import json
import logging

from django.http import HttpRequest
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from ..productionLine.dynamodb_interface import DynamodbProductionLine
from ..product.dynamodb_interface import DynamodbProducts


#_stages = ('proposed', 'ongoing', 'completed')
logger = logging.getLogger(__name__)


class ProductionLineMoveView(APIView):
    dynamodbProductionLine = DynamodbProductionLine()
    dynamodbProducts = DynamodbProducts()

    def post(self, request:HttpRequest, id : str ):

        try:
            productionItem = self.dynamodbProductionLine.getById(id=id)
# PROPOSED
            if productionItem.stage == 'proposed':
                data = {"stage" : "ongoing"}
                self.dynamodbProductionLine.updateSelfAttributes(entity=productionItem, data=data)
                #productionItem.update(actions=[ProductionLine.stage.set('ongoing')])
                return Response({'isSuccessful': 'true'}, status= status.HTTP_202_ACCEPTED)
# ONGOING
            elif productionItem.stage == 'ongoing':
                try:
                    data["attributes"] = productionItem.attributes
                    data["category"] = productionItem.category
                    data["notes"] = productionItem.notes
                    data["detail"] = productionItem.detail
                    data["name"] = productionItem.name
                    data["id"] = productionItem.id
                    key = self.dynamodbProducts.create(data=data, keepID=True)
                    #logger.debug(key)
                    self.dynamodbProductionLine.updateSelfAttributes(entity=productionItem, data={"stage" : 'completed'})

                    return Response(status= status.HTTP_202_ACCEPTED, data= {'isSuccessful': 'true', "keys" : key})
                except Exception as e:
                    logger.error(e)
                    return Response({'isSuccessful' : 'false'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    # COMPLETED        
            elif productionItem.stage == 'completed':
                    #productItem = Products.get(hash_key=productionItem.category, range_key=productionItem.id)
                if self.dynamodbProducts.checkPkExists(category=productionItem.category, id=productionItem.id):
                    return Response({'isSuccessful': 'false'}, status= status.HTTP_302_FOUND)
                else:
                    try:
                        data["attributes"] = productionItem.attributes
                        data["category"] = productionItem.category
                        data["notes"] = productionItem.notes
                        data["detail"] = productionItem.detail
                        data["name"] = productionItem.name
                        data["id"] = productionItem.id
                        key = self.dynamodbProducts.create(data=data, keepID=True)
                        #logger.debug("daal diya")
                        return Response({'isSuccessful' : 'true', 'keys' : key}, status = status.HTTP_202_ACCEPTED)
                    except Exception as e:
                        logger.error(e)
                        return Response({'isSuccessful' : 'false'}, status=status.HTTP_304_NOT_MODIFIED)

                # todo - check presence in products table. if not give message and then copy
            else:
                return Response({'isSuccessful': 'false'}, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(e)
            return Response({'isSuccessful': 'false'}, status= status.HTTP_404_NOT_FOUND)


class ProductionLinesView(APIView):
    dynamodbProductionLine = DynamodbProductionLine()

    def post(self, request : HttpRequest):

        data = request.data
        try:
            key = self.dynamodbProductionLine.create(data=data)
            # logger.debug(key)
            return Response(status=status.HTTP_201_CREATED, data={"keys" : key, "id" : key["id"]})
        except Exception as e:
            logger.exception(e)
            return Response({'error': 'Failed to insert'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request : HttpRequest):
        
        lastKey = request.query_params.get('lastKey')
        if lastKey:
            lastKey = lastKey.replace("\'", "\"")
            de = json.loads(lastKey)
            lastKey = de
        totalItemCount = request.query_params.get('totalItemCount', 0)
        limit = int(request.query_params.get('limit', 10))
        stage : str = request.query_params.get('stage', 'proposed')

# refine filter usage
        filter = request.query_params.get('filter')
        # logger.debug("filter", filter)
        if filter != None:
            filter = json.loads(filter)
            if "stage" in filter.keys():
                stage = filter["stage"]

        try:
            if stage == "all":
                products = self.dynamodbProductionLine.getPaginationByScan(limit=limit, lastKey=lastKey)
            else:
                products = self.dynamodbProductionLine.getPaginationByStageQuery(limit=limit, lastKey=lastKey, stage=stage)

            l = []
            for item in products:
                formatItem :dict = json.loads(item.to_json())
                l.append(formatItem)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        newLastKey = products.last_evaluated_key
        context = {'items' : l, "lastKey" : newLastKey, "totalItemCount" : totalItemCount + products.total_count, "limit" : limit}
        contentRange =  f"{limit}"
        return Response(status=status.HTTP_200_OK, headers={"content-range" : contentRange}, data=context)

    def delete(self, request, **kwargs):
        if "filter" in request.query_params.keys():
            filter : dict = json.loads(request.query_params.get("filter"))
        else:
            return Response({'isSuccessful': 'False', "message": "pass array of ids to delete in filter query params with key 'id"}, status= status.HTTP_400_BAD_REQUEST)
        
        ids = filter.get("id", None)
        if ids != None:
            try:
                for id in ids:
                    self.dynamodbProductionLine.delete(id)
                return Response(status=status.HTTP_200_OK, data=ids)
            except Exception as e:
                logger.exception(e)
                return Response({'isSuccessful': 'False', "ids" : ids}, status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'isSuccessful': 'False', "message": "pass array of ids to delete in filter query params with key 'id"}, status= status.HTTP_400_BAD_REQUEST)




class ProductionLineDetailView(APIView):
    dynamodbProductionLine = DynamodbProductionLine()

    def get(self, request : HttpRequest, id : str):
        try:
            item = self.dynamodbProductionLine.getById(id=id)
            data = json.loads(item.to_json())
            return Response(status=status.HTTP_200_OK, data={"item":data})
        except Exception as e:
            logger.exception(e)
            return Response({'error': "item doesn't exist"}, status= status.HTTP_404_NOT_FOUND)

    def put(self, request:HttpRequest, id:str):
        try:
            entity = self.dynamodbProductionLine.getById(id=id)
            item = self.dynamodbProductionLine.updateSelfAttributes(entity=entity, data=request.data)
            data = json.loads(item.to_json())
            return Response({'isSuccessful' : 'true', "item" : data}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.exception(e)
            return Response({'error': 'Failed to update'}, status= status.HTTP_400_BAD_REQUEST)


    def delete(self, request:HttpRequest, id : str):
        try:
            self.dynamodbProductionLine.delete(id=id)
            return Response(status=status.HTTP_202_ACCEPTED, data=id)
        except Exception as e:
            logger.exception(e)
            return Response({'error': 'Failed to delete'}, status= status.HTTP_400_BAD_REQUEST)
        

