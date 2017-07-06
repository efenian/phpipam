import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import L2DomainsApi
from lib.utils import get_l2domain_id


class DelL2domain(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        l2domains_api = L2DomainsApi(phpipam=self.ipam)

        l2dom_id = get_l2domain_id(ipam=self.ipam, name=name)

        delete_result = l2domains_api.del_l2domain(l2domain_id=l2dom_id)

        self.ipam.logout()

        return delete_result
