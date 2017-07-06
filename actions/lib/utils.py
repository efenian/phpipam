""" Utility Functions """
from lib.phpipam.controllers import L2DomainsApi
from lib.phpipam.controllers import SectionsApi
from lib.phpipam.controllers import SubnetsApi
from lib.phpipam.controllers import ToolsDevicesApi
from lib.phpipam.controllers import ToolsDeviceTypesApi
from lib.phpipam.controllers import ToolsLocationsApi
from lib.phpipam.controllers import ToolsRacksApi
from lib.phpipam.controllers import ToolsTagsApi
from lib.phpipam.controllers import VlansApi
from lib.phpipam.controllers import VRFsApi


def check_list(t_list='', t_item='', t_string=''):
    """ function to check list length and raise appropriate exception """
    not_found = t_string.capitalize() + ' not found: ' + t_item
    ambiguous = 'Abiguous ' + t_string + ' match: ' + t_item
    if len(t_list) == 0:
        raise ValueError(not_found)
    if len(t_list) > 1:
        raise ValueError(ambiguous)


def get_tools_location_id(ipam=None, name=None):
    locations_api = ToolsLocationsApi(phpipam=ipam)

    locationlist = (locations_api.list_tools_locations())['data']
    location = [x for x in locationlist if x['name'] == name]

    check_list(t_list=location, t_item=name, t_string='location')

    return location[0]['id']


def get_tools_rack_id(ipam=None, name=None):
    racks_api = ToolsRacksApi(phpipam=ipam)

    racklist = (racks_api.list_tools_racks())['data']
    rack = [x for x in racklist if x['name'] == name]

    check_list(t_list=rack, t_item=name, t_string='rack')

    return rack[0]['id']


def get_tools_devicetype_id(ipam=None, name=None):
    devicetypes_api = ToolsDeviceTypesApi(phpipam=ipam)

    devicetypelist = (devicetypes_api.list_tools_devicetypes())['data']
    dtype = [x for x in devicetypelist if x['tname'] == name]

    check_list(t_list=dtype, t_item=name, t_string='device type')

    return dtype[0]['id']


def get_tools_device_id(ipam=None, name=None):
    devices_api = ToolsDevicesApi(phpipam=ipam)

    devicelist = (devices_api.list_tools_devices())['data']
    device = [x for x in devicelist if x['hostname'] == name]

    check_list(t_list=device, t_item=name, t_string='device')

    return device[0]['id']


def get_section_id(ipam=None, name=None):
    sections_api = SectionsApi(phpipam=ipam)

    sectionlist = (sections_api.list_sections())['data']
    sect = [x for x in sectionlist if x['name'] == name]

    check_list(t_list=sect, t_item=name, t_string='section name')

    return sect[0]['id']


def get_l2domain_id(ipam=None, name=None):
    l2domains_api = L2DomainsApi(phpipam=ipam)

    l2domlist = (l2domains_api.list_l2domains())['data']
    l2dom = [x for x in l2domlist if x['name'] == name]

    check_list(t_list=l2dom, t_item=name, t_string='l2domain name')

    return l2dom[0]['id']


def get_vlan_id(ipam=None, name=None, number=None, l2domain_id=None):
    vlans_api = VlansApi(phpipam=ipam)

    vlanlist = (vlans_api.list_vlans())['data']

    if number and l2domain_id:
        vlan = [x for x in vlanlist
                if x['number'] == number and
                x['domainId'] == l2domain_id]

        check_list(t_list=vlan, t_item=number, t_string='vlan')

        return vlan[0]['id']

    if name:
        vlan = [x for x in vlanlist
                if x['name'] == name]

        check_list(t_list=vlan, t_item=name, t_string='vlan')

        return vlan[0]['id']


def get_subnet_id(ipam=None, name=None, cidr=None, section_id=None):
    subnets_api = SubnetsApi(phpipam=ipam)

    if cidr and section_id:
        subnetlist = (subnets_api.list_subnets_cidr(subnet_cidr=cidr))['data']
        subnet = [x for x in subnetlist if x['sectionId'] == section_id]

        check_list(t_list=subnet, t_item=cidr, t_string='subnet cidr')

        return subnet[0]['id']


def get_vrf_id(ipam=None, name=None):
    vrfs_api = VRFsApi(phpipam=ipam)

    vrflist = (vrfs_api.list_vrfs())['data']
    vrf = [x for x in vrflist if x['name'] == name]

    check_list(t_list=vrf, t_item=name, t_string='VRF')

    return vrf[0]['id']


def get_tag_id(ipam=None, name=None):
    tags_api = ToolsTagsApi(phpipam=ipam)

    taglist = (tags_api.list_tools_tags())['data']
    tag = [x for x in taglist if x['type'] == name]

    check_list(t_list=tag, t_item=name, t_string='tag')

    return tag[0]['id']


def get_address_id(ipam=None, ip_addr=None, subnet_id=None):
    subnets_api = SubnetsApi(phpipam=ipam)

    addresslist = (subnets_api.list_subnet_addresses(
        subnet_id=subnet_id))['data']

    addr = [x for x in addresslist if x['ip'] == ip_addr]

    check_list(t_list=addr, t_item=ip_addr, t_string='address')

    return addr[0]['id']
