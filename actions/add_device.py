import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import ToolsDevicesApi
from lib.utils import get_tools_devicetype_id
from lib.utils import get_tools_location_id
from lib.utils import get_tools_rack_id
from lib.utils import get_section_id


class AddDevice(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, hostname, ip_addr, devicetype, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        type_id = get_tools_devicetype_id(ipam=self.ipam, name=devicetype)

        if kwargs['location']:
            kwargs['location_id'] = get_tools_location_id(
                    ipam=self.ipam, name=kwargs['location'])

        if kwargs['rack']:
            kwargs['rack_id'] =  get_tools_rack_id(
                    ipam=self.ipam, name=kwargs['rack'])

        if kwargs['sections']:
            sect_names = kwargs['sections'].split(';')
            section_ids = []

            for sect_name in sect_names:
                section_ids.append(
                        get_section_id(ipam=self.ipam, name=sect_name))

            kwargs['sections'] = ';'.join(section_ids)


        devices_api = ToolsDevicesApi(phpipam=self.ipam)

        new_device = devices_api.add_tools_device(
            hostname=hostname,
            ip_addr=ip_addr,
            type_id=type_id,
            **kwargs)

        self.ipam.logout()

        return new_device
