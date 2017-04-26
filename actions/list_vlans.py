import warnings
import lib.phpipam

from st2actions.runners.pythonrunner import Action


class ListVlans(Action):
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

        tools_vlans_api = lib.phpipam.controllers.ToolsVlansApi(phpipam=ipam)

        vlanlist = tools_vlans_api.list_tools_vlans()

        ipam.logout()

        return vlanlist
