import warnings
import phpipam
import utils
import json

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

        ipam = phpipam.PhpIpam(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        l2domains = (ipam.list_l2domains())['data']
        l2dom = [x for x in l2domains if x['name'] == l2domain]
        utils.check_list(t_list=l2dom, t_item=l2domain,
                         t_string='layer 2 domain')
        l2dom_id = l2dom[0]['id']

        vlans = (ipam.list_vlans())['data']
        vlan = [x for x in vlans
                if x['number'] == number and x['domainId'] == l2dom_id]
        utils.check_list(t_list=vlan, t_item=number, t_string='vlan')
        vlan_id = vlan[0]['id']

        print json.dumps(ipam.del_vlan(vlan_id=vlan_id),
                         sort_keys=True, indent=4)

        ipam.logout()
