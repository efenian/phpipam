import warnings
import lib.phpipam
import lib.utils

from st2actions.runners.pythonrunner import Action


class AddDevice(Action):
    """ Stackstorm Python Runner """
    def run(self, hostname, ip_addr, devicetype, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(
            api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        devicetypes_api = lib.phpipam.controllers.ToolsDeviceTypesApi(
            phpipam=ipam)

        devicetypes = (devicetypes_api.list_tools_devicetypes())['data']
        dtype = [x for x in devicetypes if x['tname'] == devicetype]
        lib.utils.check_list(
            t_list=dtype, t_item=devicetype, t_string='device type')
        type_id = dtype[0]['id']

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

        devices_api = lib.phpipam.controllers.ToolsDevicesApi(phpipam=ipam)

        new_device = devices_api.add_tools_device(
            hostname=hostname,
            ip_addr=ip_addr,
            type_id=type_id,
            **kwargs)

        ipam.logout()

        return new_device
