import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsLocationsApi
from lib.utils import get_tools_location_id


class DelLocation(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        locations_api = ToolsLocationsApi(phpipam=self.ipam)

        location_id = get_tools_location_id(ipam=self.ipam, name=name)

        delete_result = locations_api.del_tools_location(
                location_id=location_id)

        self.ipam.logout()

        return delete_result
