import logging
from ...productionLine.actions.models import ProductionLineAction

logger = logging.getLogger(__name__)


class DynamodbProductionLineAction:
    if not ProductionLineAction.exists():
        ProductionLineAction.create_table(wait=True)
        logger.info("created the productionLineAction-table")

    def add(self, entity : ProductionLineAction):
        entity.save()

    def getByIpAction(self, pid : str, ipAction : str):
        entity = ProductionLineAction.get(hash_key=pid, range_key=ipAction)
        return entity

    def updateSelfActionType(self, entity : ProductionLineAction, actionVal : str):
        entity.update(actions=[ProductionLineAction.actionVal.set(actionVal)])
