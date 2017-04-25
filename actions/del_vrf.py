import warnings
import lib.phpipam
import lib.utils

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class DelDevice(Action):
    """ Stackstorm Python Runner """
    def run(self, name):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(
            api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        vrfs_api = lib.phpipam.controllers.VRFsApi(phpipam=ipam)

        vrflist = (vrfs_api.list_vrfs())['data']
        vrf = [x for x in vrflist if x['name'] == name]
        lib.utils.check_list(t_list=vrf, t_item=name, t_string='VRF')
        vrf_id = vrf[0]['id']

        delete_result = vrfs_api.del_vrf(vrf_id=vrf_id)

        ipam.logout()

        return delete_result
