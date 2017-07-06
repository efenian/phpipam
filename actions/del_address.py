import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import AddressesApi
from lib.utils import get_section_id
from lib.utils import get_subnet_id
from lib.utils import get_address_id


class DelAddress(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, section, subnet_cidr, ip_addr):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        addresses_api = AddressesApi(phpipam=self.ipam)

        sect_id = get_section_id(ipam=self.ipam, name=section)

        subnet_id = get_subnet_id(
            ipam=self.ipam, cidr=subnet_cidr, section_id=sect_id)

        addr_id = get_address_id(
            ipam=self.ipam, ip_addr=ip_addr, subnet_id=subnet_id)

        delete_result = addresses_api.del_address(address_id=addr_id)

        self.ipam.logout()

        return delete_result
