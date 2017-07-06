import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import VRFsApi


class ListVrfs(BaseAction):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        vrfs_api = VRFsApi(phpipam=self.ipam)

        vrflist = vrfs_api.list_vrfs()

        self.ipam.logout()

        return vrflist
