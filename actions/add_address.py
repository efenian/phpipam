import warnings
import lib.phpipam
import lib.utils

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class AddAddress(Action):
    """ Stackstorm Python Runner """
    def run(self, ip_addr, subnet_cidr, **kwargs):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(
            api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        section_api = lib.phpipam.controllers.SectionsApi(phpipam=ipam)

        section_data = (section_api.get_section(
            section=kwargs['section']))['data']
        sect_id = section_data['id']

        subnets_api = lib.phpipam.controllers.SubnetsApi(phpipam=ipam)

        subnetlist = (subnets_api.list_subnets_cidr(
            subnet_cidr=subnet_cidr))['data']
        sub = [x for x in subnetlist if x['sectionId'] == sect_id]
        lib.utils.check_list(t_list=sub, t_item=subnet_cidr, t_string='subnet')
        sub_id = sub[0]['id']

        tags_api = lib.phpipam.controllers.ToolsTagsApi(phpipam=ipam)

        taglist = (tags_api.list_tools_tags())['data']
        tag_match = [x for x in taglist if x['type'] == kwargs['tag']]
        lib.utils.check_list(t_list=tag_match, t_item=kwargs['tag'], t_string='tag')
        kwargs['tag_id'] = tag_match[0]['id']

        if kwargs['device'] is not None:
            devices_api = lib.phpipam.controllers.ToolsDevicesApi(phpipam=ipam)

            devicelist = (devices_api.list_tools_devices())['data']
            dev = [x for x in devicelist if x['hostname'] == kwargs['device']]
            lib.utils.check_list(
                t_list=dev, t_item=kwargs['device'], t_string='device')
            kwargs['device_id'] = dev[0]['id']

        print kwargs['device_id']

        addresses_api = lib.phpipam.controllers.AddressesApi(phpipam=ipam)

        new_address = addresses_api.add_address(
            ip_addr=ip_addr, subnet_id=sub_id, **kwargs)

        ipam.logout()

        return new_address

