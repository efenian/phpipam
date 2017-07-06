import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsRacksApi
from lib.utils import get_tools_location_id


class AddRack(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        if kwargs['location']:
            kwargs['location_id'] = get_tools_location_id(
                    ipam=self.ipam, name=kwargs['location'])

        racks_api = ToolsRacksApi(phpipam=self.ipam)

        new_rack = racks_api.add_tools_rack(name=name, **kwargs)

        self.ipam.logout()

        return new_rack
