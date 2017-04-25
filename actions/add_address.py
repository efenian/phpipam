import warnings
import lib.phpipam
import lib.utils
import json

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class AddAddress(Action):
    """ Stackstorm Python Runner """
    def run(self, ip_addr, subnet_cidr, section, tag, **kwargs):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = phpipam.controllers.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        section_api = phpipam.controller.SectionsApi(phpipam=ipam)

        section_data = (section_api.get_section(section=section))['data']
        if len(section_data):
            sect_id = sect[0]['id']

        subnets_api = phpipam.controller.SubnetsApi(phpipam=ipam)

        subnets = (subnets_api.list_subnets_cidr(subnet_cidr=subnet_cidr))['data']
        sub = [x for x in subnets if x['sectionId'] == sect_id]
        utils.check_list(t_list=sub, t_item=subnet_cidr, t_string='subnet')
        sub_id = sub[0]['id']

        tags_api = phpipam.controller.ToolsTagsApi(phpipam=ipam)

        tags = (tags_api.list_tags())['data']
        tag_list = [x for x in tags if x['type'] == tag]
        utils.check_list(t_list=tag_list, t_item=tag, t_string='tag')
        tag_id = tag_list[0]['id']

        if kwargs['device'] is not None:
            devices_api = phpipam.controller.ToolsDevicesApi(phpipam=ipam)

            devices = (devices_api.list_devices())['data']
            dev = [x for x in devices if x['hostname'] == kwargs['device']]
            utils.check_list(t_list=dev, t_item=kwargs['device'],
                             t_string='device')
            kwargs['device_id'] = dev[0]['id']


        addresses_api = phpipam.controller.AddressesApi(phpipam=ipam)

        ipam.logout()

        return ipam.add_address(ip_addr=ip_addr, subnet_id=sub_id,
                         tag_id=tag_id, **kwargs),
                         sort_keys=True, indent=4)
