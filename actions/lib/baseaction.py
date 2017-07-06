from st2actions.runners.pythonrunner import Action
from lib.phpipam import PhpIpamApi


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self.api_uri = config.get('api_uri', None)
        self.api_username = config.get('api_username', None)
        self.api_password = config.get('api_password', None)
        self.api_verify_ssl = config.get('api_verify_ssl', False)

        self.ipam = PhpIpamApi(
            api_uri=self.api_uri, api_verify_ssl=self.api_verify_ssl)
