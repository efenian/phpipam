import warnings
import lib.phpipam
import lib.utils

from st2actions.runners.pythonrunner import Action


class DelDevice(Action):
    """ Stackstorm Python Runner """
    def run(self, hostname):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(
            api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        devices_api = lib.phpipam.controllers.ToolsDevicesApi(phpipam=ipam)

        devicelist = (devices_api.list_tools_devices())['data']
        dev = [x for x in devicelist if x['hostname'] == hostname]
        lib.utils.check_list(t_list=dev, t_item=hostname, t_string='device')
        dev_id = dev[0]['id']

        delete_result = devices_api.del_tools_device(device_id=dev_id)

        ipam.logout()

        return delete_result
