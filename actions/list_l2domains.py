import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import L2DomainsApi


class ListL2domains(BaseAction):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        l2domains_api = L2DomainsApi(phpipam=self.ipam)

        l2domainlist = l2domains_api.list_l2domains()

        self.ipam.logout()

        return l2domainlist
