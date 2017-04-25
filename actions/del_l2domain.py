import warnings
import lib.phpipam
import lib.utils

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class DelL2domain(Action):
    """ Stackstorm Python Runner """
    def run(self, name):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        l2domains_api = lib.phpipam.controllers.L2DomainsApi(phpipam=ipam)

        l2domainlist = (l2domains_api.list_l2domains())['data']
        l2dom = [x for x in l2domainlist if x['name'] == name]
        lib.utils.check_list(t_list=l2dom, t_item=name, t_string='layer 2 domain')
        l2dom_id = l2dom[0]['id']

        delete_result = l2domains_api.del_l2domain(l2domain_id=l2dom_id)

        ipam.logout()

        return delete_result
