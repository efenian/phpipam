import warnings
import json

from lib.baseaction import BaseAction
from lib.phpipam.controllers import SectionsApi
from lib.utils import get_section_id


class AddSection(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name, operator_permissions, group_permissions, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        permission_map = {
            'ro': '1',
            'rw': '2',
            'rwa': '3'
        }

        self.ipam.login(auth=(self.api_username, self.api_password))

        sections_api = SectionsApi(phpipam=self.ipam)

        if kwargs['master_section']:
            kwargs['master_section_id'] = get_section_id(
                ipam=self.ipam, name=kwargs['master_section'])

        permissions = {}
        permissions['2'] = permission_map[operator_permissions]
        permissions['3'] = permission_map[group_permissions]

        kwargs['show_vlan'] = int(kwargs['show_vlan'])
        kwargs['show_vrf'] = int(kwargs['show_vrf'])
        kwargs['strict_mode'] = int(kwargs['strict_mode'])

        new_section = sections_api.add_section(
            name=name, permissions=json.dumps(permissions), **kwargs)

        self.ipam.logout()

        return new_section
