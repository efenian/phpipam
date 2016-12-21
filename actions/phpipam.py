import json
import requests


class PhpIpamException(Exception):
    """ phpipam generic exception class """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class PhpIpam(object):
    """ phpipam REST API class """
    #pylint: disable=too-many-public-methods

    _api_uri = ''
    _api_token = ''
    _api_verify_ssl = False
    _api_headers = {
        'accept': 'application/json'
    }


    def __init__(self, api_uri='', api_verify_ssl=True):
        self._api_uri = api_uri
        self._api_verify_ssl = api_verify_ssl


    def api_send_request(self, path='', method='', auth='', payload=''):
        """ send HTTP REST request """
        verify = self._api_verify_ssl
        try:
            response = requests.request(
                method=method,
                url=self._api_uri + path,
                auth=auth,
                headers=self._api_headers,
                data=payload,
                verify=verify)
        except requests.exceptions.RequestException as exception:
            print exception
        else:
            status_code = response.status_code
            if status_code == 200:
                return json.loads(response.text)
            elif status_code == 201:
                result = json.loads(response.text)
                result['location'] = response.headers['Location']
                return result
            else:
                raise PhpIpamException(response.text)


    def login(self, auth=''):
        """ authenticate to API """
        result = self.api_send_request(path='user/', auth=auth, method='post')
        self._api_token = result['data']['token']
        self._api_headers['phpipam-token'] = self._api_token


    def logout(self):
        """ delete session """
        uri = 'user/'
        self.api_send_request(path=uri, method='delete')


    def add_device(self, hostname='', ip_addr='', devicetype='', **kwargs):
        """ add new device """
        payload = {
            'hostname' : hostname,
            'ip_addr' : ip_addr,
            'type' : devicetype
        }
        if 'vendor' in kwargs:
            payload['vendor'] = kwargs['vendor']
        if 'model' in kwargs:
            payload['model'] = kwargs['model']
        if 'sections' in kwargs:
            payload['sections'] = kwargs['sections']
        if 'description' in kwargs:
            payload['description'] = kwargs['description']
        uri = 'tools/devices/'
        result = self.api_send_request(path=uri, method='post', payload=payload)
        return result


    def del_device(self, device_id=''):
        """ delete device """
        uri = 'tools/devices/' + str(device_id) + '/'
        result = self.api_send_request(path=uri, method='delete')
        return result


    def list_devices(self):
        """ get device list """
        uri = 'tools/devices/'
        result = self.api_send_request(path=uri, method='get')
        return result


    def list_devicetypes(self):
        """ get device type list """
        uri = 'tools/devicetypes/'
        result = self.api_send_request(path=uri, method='get')
        return result


    def add_l2domain(self, name='', **kwargs):
        """ add new l2domain """
        payload = {
            'name' : name
        }
        if 'description' in kwargs:
            payload['description'] = kwargs['description']
        uri = 'l2domains/'
        result = self.api_send_request(path=uri, method='post', payload=payload)
        return result


    def del_l2domain(self, l2domain_id=''):
        """ delete l2domain """
        uri = 'l2domains/' + str(l2domain_id) + '/'
        result = self.api_send_request(path=uri, method='delete')
        return result


    def list_l2domains(self):
        """ get l2domain list """
        uri = 'l2domains/'
        result = self.api_send_request(path=uri, method='get')
        return result


    def add_vlan(self, name='', number='', **kwargs):
        """ add new vlan """
        payload = {
            'name' : name,
            'number': str(number)
        }
        if 'description' in kwargs:
            payload['description'] = kwargs['description']
        if 'domain_id' in kwargs:
            payload['domainId'] = str(kwargs['domain_id'])
        uri = 'vlans/'
        result = self.api_send_request(path=uri, method='post', payload=payload)
        return result


    def del_vlan(self, vlan_id=''):
        """ delete vlan """
        uri = 'vlans/' + str(vlan_id) + '/'
        result = self.api_send_request(path=uri, method='delete')
        return result


    def list_vlans(self):
        """ get vlan list """
        uri = 'tools/vlans/'
        result = self.api_send_request(path=uri, method='get')
        return result


    def add_section(self, name='', permissions='', **kwargs):
        """ add new section """
        payload = {
            'name' : name,
            'permissions': permissions
        }
        if 'description' in kwargs:
            payload['description'] = kwargs['description']
        if 'master_section' in kwargs:
            if 'master_section' != '0':
                payload['masterSection'] = kwargs['master_section']
        if 'vlan' in kwargs:
            payload['showVLAN'] = kwargs['vlan']
        if 'vrf' in kwargs:
            payload['showVRF'] = kwargs['vrf']
        if 'strict_mode' in kwargs:
            payload['strictMode'] = kwargs['strict_mode']
        if 'ordering' in kwargs:
            payload['subnetOrdering'] = kwargs['ordering']
        uri = 'sections/'
        result = self.api_send_request(path=uri, method='post', payload=payload)
        return result


    def del_section(self, section_id=''):
        """ delete section """
        uri = 'sections/' + str(section_id) + '/'
        result = self.api_send_request(path=uri, method='delete')
        return result


    def list_sections(self):
        """ get section list """
        uri = 'sections/'
        result = self.api_send_request(path=uri, method='get')
        return result


    def get_subnet(self, subnet_id=''):
        """ get subnet details based on ID """
        uri = 'subnets/' + str(subnet_id) + '/'
        result = self.api_send_request(path=uri, method='get')
        return result

    def add_subnet(self, subnet='', mask='', section='',
                   permissions='', **kwargs):
        """ add new subnet """
        payload = {
            'subnet' : subnet,
            'mask': mask,
            'sectionId': section,
            'permissions': permissions
        }
        if 'description' in kwargs:
            payload['description'] = kwargs['description']
        if 'master_subnet' in kwargs:
            if 'master_subnet' != '0':
                payload['masterSubnetId'] = kwargs['master_subnet']
        if 'vlan' in kwargs:
            payload['vlanId'] = kwargs['vlan']
        if 'device' in kwargs:
            payload['device'] = kwargs['device']
        if 'show_name' in kwargs:
            payload['showName'] = kwargs['show_name']
        if 'ping_subnet' in kwargs:
            payload['pingSubnet'] = kwargs['ping_subnet']
        if 'discover_subnet' in kwargs:
            payload['discoverSubnet'] = kwargs['discover_subnet']
        if 'scan_agent' in kwargs:
            payload['scanAgent'] = kwargs['scan_agent']
        if 'full' in kwargs:
            payload['isFull'] = kwargs['full']
        uri = 'subnets/'
        result = self.api_send_request(path=uri, method='post', payload=payload)
        return result

    def del_subnet(self, subnet_id=''):
        """ delete subnet """
        uri = 'subnets/' + str(subnet_id) + '/'
        result = self.api_send_request(path=uri, method='delete')
        return result

    def list_subnets(self, section_id=''):
        """ get section subnet list """
        uri = 'sections/' + section_id + '/subnets/'
        result = self.api_send_request(path=uri, method='get')
        return result

    def list_subnets_cidr(self, subnet_cidr=''):
        """ lists subnets based on CIDR notation """
        uri = 'subnets/cidr/' + subnet_cidr
        result = self.api_send_request(path=uri, method='get')
        return result


    def get_subnet_first_free_address(self, subnet_id=''):
        """ get first available addresss in subnet """
        uri = 'subnets/' + str(subnet_id) + '/first_free/'
        result = self.api_send_request(path=uri, method='get')
        return result


    def add_address(self, subnet_id='', ip_addr='', tag_id='', **kwargs):
        """ add IP address """
        payload = {
            'subnetId' : str(subnet_id),
            'ip' : ip_addr,
            'tag' : tag_id
        }
        if 'hostname' in kwargs:
            payload['hostname'] = kwargs['hostname']
        if 'owner' in kwargs:
            payload['owner'] = kwargs['owner']
        if 'description' in kwargs:
            payload['description'] = kwargs['description']
        if 'note' in kwargs:
            payload['note'] = kwargs['note']
        if 'device_id' in kwargs:
            payload['deviceId'] = kwargs['device_id']
        if 'is_gateway' in kwargs:
            payload['is_gateway'] = kwargs['is_gateway']
        if 'mac' in kwargs:
            payload['mac'] = kwargs['mac']
        uri = 'addresses/'
        result = self.api_send_request(path=uri, method='post', payload=payload)
        return result

    def list_subnet_addresses(self, subnet_id=''):
        """ get list of addresses in subnet """
        uri = 'subnets/' + str(subnet_id) + '/addresses/'
        result = self.api_send_request(path=uri, method='get')
        return result


    def del_address(self, address_id=''):
        """ delete IP address """
        uri = 'addresses/' + str(address_id) + '/'
        result = self.api_send_request(path=uri, method='delete')
        return result


    def list_tags(self):
        """ get device list """
        uri = 'tools/tags/'
        result = self.api_send_request(path=uri, method='get')
        return result


#    def get_address_id(self, address=''):
#        """ get address ID """
#        uri = 'addresses/search/' + address + '/'
#        result = self.api_send_request(path=uri, method='get')
#        data = result
#
#
#    def get_first_subnet(self, subnet_id='', mask=''):
#        """ get first nested subnet """
#        uri = 'subnets/' + subnet_id + '/first_subnet/' + str(mask) + '/'
#        result = self.api_send_request(path=uri, method='get')
#        return result
