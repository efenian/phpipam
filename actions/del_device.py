import warnings
import phpipam
import utils
import json

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class DelDevice(Action):
    """ Stackstorm Python Runner """
    def run(self, hostname):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = phpipam.PhpIpam(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        devices = (ipam.list_devices())['data']
        dev = [x for x in devices if x['hostname'] == hostname]
        utils.check_list(t_list=dev, t_item=hostname, t_string='device')
        dev_id = dev[0]['id']

        print json.dumps(ipam.del_device(device_id=dev_id),
                         sort_keys=True, indent=4)

        ipam.logout()
