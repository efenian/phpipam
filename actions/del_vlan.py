import warnings
import lib.phpipam
import lib.utils

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class DelVlan(Action):
    """ Stackstorm Python Runner """
    def run(self, number, l2domain):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(
            api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        l2domains_api = lib.phpipam.controllers.L2DomainsApi(phpipam=ipam)

        l2domains = (l2domains_api.list_l2domains())['data']
        l2dom = [x for x in l2domains if x['name'] == l2domain]
        lib.utils.check_list(t_list=l2dom, t_item=l2domain,
                         t_string='layer 2 domain')
        l2dom_id = l2dom[0]['id']

        tools_vlans_api = lib.phpipam.controllers.ToolsVlansApi(phpipam=ipam)

        vlans = (tools_vlans_api.list_tools_vlans())['data']
        vlan = [x for x in vlans
                if x['number'] == number and x['domainId'] == l2dom_id]
        lib.utils.check_list(t_list=vlan, t_item=number, t_string='vlan')
        vlan_id = vlan[0]['id']

        vlans_api = lib.phpipam.controllers.VlansApi(phpipam=ipam)

        delete_result = vlans_api.del_vlan(vlan_id=vlan_id)

        ipam.logout()

        return delete_result
