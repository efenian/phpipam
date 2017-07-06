import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsRacksApi


class ListRacks(BaseAction):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        racks_api = ToolsRacksApi(phpipam=self.ipam)

        racklist = racks_api.list_tools_racks()

        self.ipam.logout()

        return racklist
