import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import SubnetsApi
from lib.utils import get_section_id
from lib.utils import get_subnet_id


class DelSubnet(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, section, subnet_cidr):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        subnets_api = SubnetsApi(phpipam=self.ipam)

        sect_id = get_section_id(ipam=self.ipam, name=section)

        sub_id = get_subnet_id(
            ipam=self.ipam, cidr=subnet_cidr, section_id=sect_id)

        delete_result = subnets_api.del_subnet(subnet_id=sub_id)

        self.ipam.logout()

        return delete_result
