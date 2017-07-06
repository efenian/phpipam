import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import VlansApi
from lib.utils import get_l2domain_id
from lib.utils import get_vlan_id


class DelVlan(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, number, l2domain):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        l2domain_id = get_l2domain_id(ipam=self.ipam, name=l2domain)
        vlan_id = get_vlan_id(
            ipam=self.ipam, number=number, l2domain_id=l2domain_id)

        vlans_api = VlansApi(phpipam=self.ipam)

        delete_result = vlans_api.del_vlan(vlan_id=vlan_id)

        self.ipam.logout()

        return delete_result
