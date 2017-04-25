import warnings
import lib.phpipam
import lib.utils

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

        ipam = lib.phpipam.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        sections_api = lib.phpipam.controllers.SectionsApi(phpipam=ipam)
        subnets_api = lib.phpipam.controllers.SubnetsApi(phpipam=ipam)

        sectionlist = (sections_api.list_sections())['data']
        sect = [x for x in sectionlist if x['name'] == section]
        lib.utils.check_list(t_list=sect, t_item=section, t_string='section name')
        sect_id = sect[0]['id']

        subnetlist = (subnets_api.list_subnets_cidr(subnet_cidr=subnet_cidr))['data']
        sub = [x for x in subnetlist if x['sectionId'] == sect_id]
        lib.utils.check_list(t_list=sub, t_item=subnet_cidr, t_string='subnet')
        sub_id = sub[0]['id']

        delete_result = subnets_api.del_subnet(subnet_id=sub_id)

        ipam.logout()

        return delete_result

