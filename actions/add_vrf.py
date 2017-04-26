import warnings
import lib.phpipam
import lib.utils

from st2actions.runners.pythonrunner import Action


class AddVrf(Action):
    """ Stackstorm Python Runner """
    def run(self, name, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(
            api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        if kwargs['sections'] is not None:
            sect_names = kwargs['sections'].split(';')

            sections_api = lib.phpipam.controllers.SectionsApi(phpipam=ipam)

            sections = (sections_api.list_sections())['data']
            section_ids = []

            for sect_name in sect_names:
                sect = [x for x in sections if x['name'] == sect_name]
                lib.utils.check_list(
                    t_list=sect, t_item=sect_name, t_string='section_name')
                section_ids.append(sect[0]['id'])

            kwargs['sections'] = ';'.join(section_ids)

        vrfs_api = lib.phpipam.controllers.VRFsApi(phpipam=ipam)

        new_vrf = vrfs_api.add_vrf(name=name, **kwargs)

        ipam.logout()

        return new_vrf
