import warnings
import lib.phpipam
import lib.utils
import json

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class AddSection(Action):
    """ Stackstorm Python Runner """
    def run(self, name, operator_permissions, group_permissions, **kwargs):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        sections_api = lib.phpipam.controllers.SectionsApi(phpipam=ipam)

        if kwargs['master_section'] is not None:
            msect = kwargs['master_section']
            sectionlist = (sections_api.list_sections())['data']
            sect = [x for x in sectionlist if x['name'] == msect]
            lib.utils.check_list(t_list=sect, t_item=msect,
                             t_string='master section')
            kwargs['master_section_id'] = sect[0]['id']

        permissions = {}

        if operator_permissions == 'ro':
            permissions['2'] = '1'
        elif operator_permissions == 'rw':
            permissions['2'] = '2'
        elif operator_permissions == 'rwa':
            permissions['2'] = '3'

        if group_permissions == 'ro':
            permissions['3'] = '1'
        elif group_permissions == 'rw':
            permissions['3'] = '2'
        elif group_permissions == 'rwa':
            permissions['3'] = '3'

        new_section = sections_api.add_section(
            name=name, permissions=json.dumps(permissions), **kwargs)

        ipam.logout()

        return new_section

