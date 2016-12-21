import warnings
import phpipam
import utils
import json

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class DelSubnet(Action):
    """ Stackstorm Python Runner """
    def run(self, section, subnet_cidr):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = phpipam.PhpIpam(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        sections = (ipam.list_sections())['data']
        sect = [x for x in sections if x['name'] == section]
        utils.check_list(t_list=sect, t_item=section, t_string='section name')
        sect_id = sect[0]['id']

        subnets = (ipam.list_subnets_cidr(subnet_cidr=subnet_cidr))['data']
        sub = [x for x in subnets if x['sectionId'] == sect_id]
        utils.check_list(t_list=sub, t_item=subnet_cidr, t_string='subnet')
        sub_id = sub[0]['id']

        print json.dumps(ipam.del_subnet(subnet_id=sub_id),
                         sort_keys=True, indent=4)

        ipam.logout()

