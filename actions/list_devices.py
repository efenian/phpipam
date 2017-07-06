import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsDevicesApi


class ListDevices(BaseAction):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        devices_api = ToolsDevicesApi(phpipam=self.ipam)

        devicelist = devices_api.list_tools_devices()

        self.ipam.logout()

        return devicelist
