import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsLocationsApi


class AddLocation(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        locations_api = ToolsLocationsApi(phpipam=self.ipam)

        new_location = locations_api.add_tools_location(name=name, **kwargs)

        self.ipam.logout()

        return new_location
