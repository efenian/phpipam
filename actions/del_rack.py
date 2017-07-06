import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsRacksApi
from lib.utils import get_tools_rack_id

class DelRack(BaseAction):
    """ Stact2 run phpipam.add_rack name="R1" size=42 location="DC2"storm Python Runner """
    def run(self, name):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        racks_api = ToolsRacksApi(phpipam=self.ipam)

        rack_id = get_tools_rack_id(ipam=self.ipam, name=name)

        delete_result = racks_api.del_tools_rack(
                rack_id=rack_id)

        self.ipam.logout()

        return
