import warnings
import lib.phpipam

from st2actions.runners.pythonrunner import Action


class ListVrfs(Action):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(
            api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        vrfs_api = lib.phpipam.controllers.VRFsApi(phpipam=ipam)

        vrflist = vrfs_api.list_vrfs()

        ipam.logout()

        return vrflist