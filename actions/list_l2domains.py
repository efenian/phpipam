import warnings
import phpipam
import json

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class ListL2domains(Action):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = phpipam.PhpIpam(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        print json.dumps(ipam.list_l2domains(), sort_keys=True, indent=4)

        ipam.logout()

