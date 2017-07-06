import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import SectionsApi
from lib.utils import get_section_id


class ListSubnets(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, section):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        sections_api = SectionsApi(phpipam=self.ipam)

        sect_id = get_section_id(ipam=self.ipam, name=section)

        subnetlist = sections_api.list_section_subnets(section_id=sect_id)

        self.ipam.logout()

        return subnetlist
