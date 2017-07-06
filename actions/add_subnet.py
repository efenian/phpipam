import warnings
import json

from lib.baseaction import BaseAction
from lib.phpipam.controllers import SubnetsApi
from lib.utils import get_subnet_id
from lib.utils import get_section_id
from lib.utils import get_l2domain_id
from lib.utils import get_vlan_id
from lib.utils import get_tools_device_id
from lib.utils import get_vrf_id
from lib.utils import get_tools_location_id


class AddSubnet(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, subnet, mask,
            operator_permissions, group_permissions, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        permission_map = {
            'ro': '1',
            'rw': '2',
            'rwa': '3'
        }
        self.ipam.login(auth=(self.api_username, self.api_password))

        subnets_api = SubnetsApi(phpipam=self.ipam)

        kwargs['section_id'] = get_section_id(
            ipam=self.ipam, name=kwargs['section'])

        if kwargs['master_subnet']:
            kwargs['master_subnet_id'] = get_subnet_id(
                ipam=self.ipam, cidr=kwargs['master_subnet'],
                section_id=kwargs['section_id'])

        if kwargs['vlan']:
            if kwargs['l2domain']:
                raise ValueError(
                    'If VLAN number is specified then ' +
                    'Layer 2 domain must also be set!')

            l2dom_id = get_l2domain_id(ipam=self.ipam, name=kwargs['l2domain'])

            kwargs['vlan_id'] = get_vlan_id(
                ipam=self.ipam, number=kwargs['vlan'], l2domain_id=l2dom_id)

        if kwargs['device']:
            kwargs['device_id'] = get_tools_device_id(
                ipam=self.ipam, name=kwargs['device'])

        if kwargs['threshold']:
            if kwargs['threshold'] < 1 or kwargs['threshold'] > 100:
                raise ValueError('Threshold should be between 1 and 100')

        if kwargs['vrf']:
            kwargs['vrf_id'] = get_vrf_id(
                ipam=self.ipam, name=kwargs['vrf'])

        if kwargs['location']:
            kwargs['location_id'] = get_tools_location_id(
                ipam=self.ipam, name=kwargs['location'])

        if (
                (kwargs['ping_subnet'] or
                 kwargs['discover_subnet']) and
                (kwargs['scan_agent'] is None or
                 kwargs['scan_agent'] == '0')):
            kwargs['scan_agent_id'] = '1'

        permissions = {}

        permissions['2'] = permission_map[operator_permissions]
        permissions['3'] = permission_map[group_permissions]

        kwargs['show_name'] = int(kwargs['show_name'])
        kwargs['ping_subnet'] = int(kwargs['ping_subnet'])
        kwargs['discover_subnet'] = int(kwargs['discover_subnet'])
        kwargs['full'] = int(kwargs['full'])

        new_subnet = subnets_api.add_subnet(
            subnet=subnet,
            mask=mask,
            permissions=json.dumps(permissions),
            **kwargs)

        self.ipam.logout()

        return new_subnet
