import warnings
import lib.phpipam
import lib.utils
import json

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class AddSubnet(Action):
    """ Stackstorm Python Runner """
    def run(self, subnet, mask, section,
            operator_permissions, group_permissions, **kwargs):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        sections_api = lib.phpipam.controllers.SectionsApi(phpipam=ipam)

        sectionlist = (sections_api.list_sections())['data']
        sect = [x for x in sectionlist if x['name'] == section]
        lib.utils.check_list(t_list=sect, t_item=section, t_string='section name')
        kwargs['section_id'] = sect[0]['id']

        subnets_api = lib.phpipam.controllers.SubnetsApi(phpipam=ipam)

        if kwargs['master_subnet'] is not None:
            msub = kwargs['master_subnet']
            subnetlist = (subnets_api.list_subnets_cidr(subnet_cidr=msub))['data']
            sub = [x for x in subnetlist if x['sectionId'] == sect[0]['id']]
            lib.utils.check_list(t_list=sub, t_item=msub, t_string='master subnet')
            kwargs['master_subnet_id'] = sub[0]['id']

        if kwargs['vlan'] is not None:
            if kwargs['l2domain'] is None:
                raise ValueError('If VLAN number is specified then ' +
                                'Layer 2 domain must also be set!')

            l2domains_api = lib.phpipam.controllers.L2DomainsApi(phpipam=ipam)
            tools_vlans_api = lib.phpipam.controllers.ToolsVlansApi(phpipam=ipam)

            l2domain = kwargs['l2domain']
            l2domainlist = (l2domains_api.list_l2domains())['data']
            l2dom = [x for x in l2domainlist if x['name'] == l2domain]
            lib.utils.check_list(t_list=l2dom, t_item=l2domain,
                             t_string='layer 2 domain')
            l2dom_id = l2dom[0]['id']

            vlan_num = kwargs['vlan']
            vlans = (tools_vlans_api.list_tools_vlans())['data']
            vlan = [x for x in vlans
                    if x['number'] == vlan_num and x['domainId'] == l2dom_id]
            lib.utils.check_list(t_list=vlan, t_item=vlan_num, t_string='vlan')
            kwargs['vlan_id'] = vlan[0]['id']

        if kwargs['device'] is not None:
            devices_api = lib.phpipam.controllers.ToolsDevicesApi(phpipam=ipam)

            device = kwargs['device']
            devicelist = (devices_api.list_tools_devices())['data']
            dev = [x for x in devicelist if x['name'] == device]
            lib.utils.check_list(t_list=dev, t_item=device, t_string='device')
            kwargs['device_id'] = dev[0]['id']

        if ((kwargs['ping_subnet'] is not None or
            kwargs['discover_subnet'] is not None) and
            (kwargs['scan_agent'] is None or kwargs['scan_agent'] == '0')):
            kwargs['scan_agent_id'] = '1'

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

        new_subnet = subnets_api.add_subnet(
            subnet=subnet,
            mask=mask,
            permissions=json.dumps(permissions),
            **kwargs)

        ipam.logout()

        return new_subnet

