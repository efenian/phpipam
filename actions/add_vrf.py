import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import VRFsApi
from lib.utils import get_section_id


class AddVrf(BaseAction):
    """ Stackstorm Python Runner """
    def run(self, name, **kwargs):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        if kwargs['sections'] is not None:
            sect_names = kwargs['sections'].split(';')

            section_ids = []

            for sect_name in sect_names:
                section_ids.append(get_section_id(
                    ipam=self.ipam, name=sect_name))

            kwargs['sections'] = ';'.join(section_ids)

        vrfs_api = VRFsApi(phpipam=self.ipam)

        new_vrf = vrfs_api.add_vrf(name=name, **kwargs)

        self.ipam.logout()

        return new_vrf
