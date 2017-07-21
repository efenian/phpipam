import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import AddressesApi
from lib.utils import get_section_id
from lib.utils import get_subnet_id
from lib.utils import get_tag_id
from lib.utils import get_tools_device_id


class AddAddressFirstFree(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, subnet_cidr, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        sect_id = get_section_id(ipam=self.ipam, name=kwargs['section'])

        subnet_id = get_subnet_id(
            ipam=self.ipam, cidr=subnet_cidr, section_id=sect_id)

        kwargs['tag_id'] = get_tag_id(ipam=self.ipam, name=kwargs['tag'])

        if kwargs['device']:
            kwargs['device_id'] = get_tools_device_id(
                ipam=self.ipam, name=kwargs['device'])

        addresses_api = AddressesApi(phpipam=self.ipam)

        new_address = addresses_api.add_address_first_free(
            subnet_id=subnet_id, **kwargs)

        self.ipam.logout()

        return new_address
