import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsLocationsApi


class ListLocations(BaseAction):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        locations_api = ToolsLocationsApi(phpipam=self.ipam)

        locationlist = locations_api.list_tools_locations()

        self.ipam.logout()

        return locationlist
