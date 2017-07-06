import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import VRFsApi
from lib.utils import get_vrf_id


class DelDevice(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        vrfs_api = VRFsApi(phpipam=self.ipam)

        vrf_id = get_vrf_id(ipam=self.ipam, name=name)

        delete_result = vrfs_api.del_vrf(vrf_id=vrf_id)

        self.ipam.logout()

        return delete_result
