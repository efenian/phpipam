import warnings
import lib.phpipam

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class AddL2domain(Action):
    """ Stackstorm Python Runner """
    def run(self, name, **kwargs):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        l2domains_api = lib.phpipam.controllers.L2DomainsApi(phpipam=ipam)

        new_l2domain = l2domains_api.add_l2domain(name=name, **kwargs)

        ipam.logout()

        return new_l2domain

