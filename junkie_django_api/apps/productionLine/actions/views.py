#import json
#from django.shortcuts import render
#from django.http import HttpResponse
import logging
from rest_framework import status
#from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ...productionLine.actions.dynamodb_interface import DynamodbProductionLineAction
from ...productionLine.dynamodb_interface import DynamodbProductionLine

from .models import ProductionLineAction

logger = logging.getLogger(__name__)


def parseVal(str):
    if str == "low" or 1:
        return 1
    elif str == "mid" or 2:
        return 2
    elif str == "high" or 3:
        return 3
    elif str == "0" or 0:
        return 0
    elif type(str) == int:
        return str
    else:
        pass



# Create your views here.
class ProductionLineActionView(APIView):
    dynamodbProductionLine = DynamodbProductionLine()
    dynamodbProductionAction = DynamodbProductionLineAction()

    def post(self, request, pId):
        actionType : str = request.data['actionType']
        ip :str = request.get_host()
        actionValue = request.data.get('actionValue')
        newVal = parseVal(request.data.get('actionValue'))
        ipAction = ip + "_" + actionType


        try:
            product = self.dynamodbProductionLine.getById(id=pId)
            x = float(product.wtdPriority)
            n = int(product.priorityCount)
        except Exception as e:
            logger.exception(e)
            return Response({"error" : "Product Not Found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            entry = self.dynamodbProductionAction.getByIpAction(pId=pId, ipAction=ipAction)
            entryExist = True
        except Exception as e:
            logger.error(e)
            entryExist = False

        if entryExist:
            if actionType == 'vote':
                return Response({"isSuccessful" : "false", "message" : "already voted"}, status=status.HTTP_208_ALREADY_REPORTED)
            elif actionType == 'priority':
                oldVal = parseVal(entry.actionVal)
                if oldVal != newVal:
                    val = (x*n - oldVal + newVal)/(n+1)
                    data = {"wtdPriority" : val, "priorityCount" : n+1}
                    self.dynamodbProductionLine.updateSelfAttributes(entity=product, data=data)
                    self.dynamodbProductionAction.updateSelfActionType(entity=entry, actionVal=newVal)
                    return Response({"isSuccessful" : "true"}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"isSuccessful" : "false", "message" : "already given priority"}, status=status.HTTP_208_ALREADY_REPORTED)
            else:
                return Response({"isSuccessful" : "false", "message" : f"{actionType} is not supported"}, status=status.HTTP_404_NOT_FOUND)
        else:
            newEntry = ProductionLineAction()
            newEntry.pId = pId
            newEntry.ipAction = ipAction
            newEntry.actionVal = actionValue
            self.dynamodbProductionAction.add(entity=newEntry)
            if actionType == 'vote':
                voteCount = product.voteCount + 1
                self.dynamodbProductionLine.updateSelfAttributes(entity=product, data={"voteCount" : voteCount})
            elif actionType == 'priority':
                val = (x * n + newVal)/(n+1)
                data = {"wtdPriority" : val, "priorityCount" : n+1}
                self.dynamodbProductionLine.updateSelfAttributes(entity=product, data=data)
            return Response({"issuccessful" : "true"}, status=status.HTTP_202_ACCEPTED)
