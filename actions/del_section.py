import warnings
import phpipam
import utils
import json

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class DelSection(Action):
    """ Stackstorm Python Runner """
    def run(self, name):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = phpipam.PhpIpam(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        sections = (ipam.list_sections())['data']
        sect = [x for x in sections if x['name'] == name]
        utils.check_list(t_list=sect, t_item=name, t_string='section name')
        sect_id = sect[0]['id']

        print json.dumps(ipam.del_section(section_id=sect_id),
                         sort_keys=True, indent=4)

        ipam.logout()
