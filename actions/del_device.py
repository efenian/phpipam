import warnings
import lib.phpipam
import lib.utils

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsDevicesApi
from lib.utils import get_tools_device_id


class DelDevice(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, hostname):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        devices_api = ToolsDevicesApi(phpipam=self.ipam)

        dev_id = get_tools_device_id(ipam=self.ipam, name=hostname)

        delete_result = devices_api.del_tools_device(device_id=dev_id)

        self.ipam.logout()

        return delete_result
