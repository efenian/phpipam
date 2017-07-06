import warnings

from lib.baseaction import BaseAction
from lib.phpipam.controllers import SectionsApi


class ListSections(BaseAction):
    """ Stackstorm Python Runner """
    def run(self):
        """ Stackstorm Run Method  """
        warnings.filterwarnings('ignore')

        self.ipam.login(auth=(self.api_username, self.api_password))

        sections_api = SectionsApi(phpipam=self.ipam)

        sectionlist = sections_api.list_sections()

        self.ipam.logout()

        return sectionlist
