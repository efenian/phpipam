import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import L2DomainsApi


class AddL2domain(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        l2domains_api = L2DomainsApi(phpipam=self.ipam)

        new_l2domain = l2domains_api.add_l2domain(name=name, **kwargs)

        self.ipam.logout()

        return new_l2domain
