import warnings
import lib.phpipam
import lib.utils

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

        ipam = lib.phpipam.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        sections_api = lib.phpipam.controllers.SectionsApi(phpipam=ipam)

        sectionlist = (sections_api.list_sections())['data']
        sect = [x for x in sectionlist if x['name'] == name]
        lib.utils.check_list(t_list=sect, t_item=name, t_string='section name')
        sect_id = sect[0]['id']

        delete_result = sections_api.del_section(section_id=sect_id)

        ipam.logout()

        return delete_result
