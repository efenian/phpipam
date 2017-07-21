import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import VlansApi
from lib.utils import get_l2domain_id


class AddVlan(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name, number, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        if kwargs['l2domain']:
            kwargs['domain_id'] = get_l2domain_id(
                ipam=self.ipam, name=kwargs['l2domain'])

        vlans_api = VlansApi(phpipam=self.ipam)

        new_vlan = vlans_api.add_vlan(name=name, number=number, **kwargs)

        self.ipam.logout()

        return new_vlan
