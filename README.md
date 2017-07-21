Stackstorm pack for {php}IPAM
======


Here is what you need:

  - [Stackstorm](https://docs.stackstorm.com/install/index.html#installation)
  - [{php}IPAM 1.3](http://phpipam.net/documents/download-phpipam/) (you can try my [vagrant](https://github.com/efenian/phpipamvagrant) as well)

You will have to enable the phpipam API and have mod_rewrite working.

The phpipam API configuration should be placed in the phpipam.yaml file in the stackstom configuration directory.  I have only implimented the None and SSL API security methods, I have not yet implimented crypt support.  SSL method is recommended for encryption.

### Sample phpipam.yaml

phpipam API app id is set to app in this case


```yaml
---
    api_uri: "https://192.168.16.30/api/app/"
    api_username: "admin"
    api_password: "password"
    api_verify_ssl: False
```

### Examples

#### Add/List/Remove location(s):

```sh
st2 run phpipam.add_location name="SV2" address="1350 Duane Avenue, Santa Clara, CA 95054"
st2 run phpipam.add_location name="DC2" address="21715 Filigree Court, Ashburn, VA 20147"
```

```sh
st2 run phpipam.list_locations
```

```sh
st2 run phpipam.del_location name="SV2"
```

#### Add/List/Remove rack(s):

```sh
st2 run phpipam.add_rack name="R1.DC2" size=42 location="DC2"
st2 run phpipam.add_rack name="R2.DC2" size=42 location="DC2"
```

```sh
st2 run phpipam.list_racks
```

```sh
st2 run phpipam.del_rack name="R2.DC2"
```

#### Add/List/Remove device(s):

```sh
st2 run phpipam.add_device hostname="SPINE1.DC2" ip_addr="198.18.0.1" devicetype="Switch" rack="R1.DC2" rack_size="2" rack_start="41" location="DC2" sections="Customers;IPv6"
st2 run phpipam.add_device hostname="LEAF1.DC2" ip_addr="198.18.0.1" devicetype="Switch" rack="R1.DC2" rack_size="2" rack_start="39" location="DC2" sections="Customers;IPv6"
```

```sh
st2 run phpipam.list_devices
```

```sh
st2 run phpipam.del_device hostname="LEAF1.DC2"
```

#### Add/List/Remove Layer 2 domain(s):

```sh
st2 run phpipam.add_l2domain name="SV2" description="santa clara"
st2 run phpipam.add_l2domain name="DC2" description="ashburn"
```

```sh
st2 run phpipam.list_l2domains
```

```sh
st2 run phpipam.del_l2domain name="SV2"
```

#### Add/List/Remove VLAN(s):

```sh
st2 run phpipam.add_vlan name="tenant1" number="100" description="my new tenant vlan" l2domain="DC2"
```

```sh
st2 run phpipam.list_vlans
```

```sh
st2 run phpipam.del_vlan number="100" l2domain="DC2"
```

#### Add/List/Remove Section:

```sh
st2 run phpipam.add_section name="parent" group_permissions="ro" operator_permissions="rw"
```

```sh
st2 run phpipam.add_section name="child" group_permissions="ro" operator_permissions="rw" master_section="parent"
```

```sh
st2 run phpipam.list_sections
```

```sh
st2 run phpipam.del_section name="child"
```

```sh
 st2 run phpipam.del_section name="parent"
```

#### Add/List/Remove Subnet(s):

```sh
st2 run phpipam.add_subnet subnet="172.16.0.0" mask="12" section="Customers" description="RFC1918 Space" group_permissions="ro" operator_permissions="rw"
```

```sh
st2 run phpipam.add_subnet subnet="172.16.0.0" mask="24" section="Customers" description="RFC1918 Space" group_permissions="ro" operator_permissions="rw" master_subnet="172.16.0.0/12"
```

```sh
st2 run phpipam.add_subnet subnet="172.16.0.0" mask="31" section="Customers" description="RFC1918 Space" group_permissions="ro" operator_permissions="rw" master_subnet="172.16.0.0/24"
```

```sh
st2 run phpipam.add_subnet subnet="172.16.0.2" mask="31" section="Customers" description="RFC1918 Space" group_permissions="ro" operator_permissions="rw" master_subnet="172.16.0.0/24"
```

```sh
st2 run phpipam.add_subnet_first_free master_subnet="172.16.0.0/24" mask="31" section="Customers" description="RFC1918 Space" group_permissions="ro" operator_permissions="rw"
```

```sh
st2 run phpipam.list_subnets section="Customers"
```

```sh
st2 run phpipam.del_subnet section="Customers" subnet_cidr="172.16.0.4/31"
```

```sh
st2 run phpipam.del_subnet section="Customers" subnet_cidr="172.16.0.2/31"
```

```sh
st2 run phpipam.del_subnet section="Customers" subnet_cidr="172.16.0.0/31"
```

```sh
st2 run phpipam.del_subnet section="Customers" subnet_cidr="172.16.0.0/24"
```

```sh
st2 run phpipam.del_subnet section="Customers" subnet_cidr="172.16.0.0/12"
```

#### Get First Free IP from Subnet:

```sh
st2 run phpipam.get_subnet_first_free_address section="Customers" subnet_cidr="10.10.1.0/24"
```

#### Add/List/Remove IP address(es):

```sh
st2 run phpipam.add_address section="Customers" subnet_cidr="10.10.1.0/24" ip_addr="10.10.1.1" hostname="ETH-1/1.SPINE1.DC2" description="ETH-1/1" is_gateway="0" tag="Used" mac="aa:bb:cc:dd:ee:f1" owner="INFRA" device="SPINE1.DC2" note="SPINE1-LEAF1"
```

```sh
st2 run phpipam.add_address section="Customers" subnet_cidr="10.10.1.0/24" ip_addr="10.10.1.2" hostname="ETH-1/2.SPINE1.DC2" description="ETH-1/2" is_gateway="0" tag="Used" mac="aa:bb:cc:dd:ee:f2" owner="INFRA" device="SPINE1.DC2" note="SPINE1-LEAF2"
```

```sh
st2 run phpipam.list_subnet_addresses section="Customers" subnet_cidr="10.10.1.0/24"
```

```sh
st2 run phpipam.del_address section="Customers" subnet_cidr="10.10.1.0/24" ip_addr="10.10.1.1"
```

```sh
st2 run phpipam.del_address section="Customers" subnet_cidr="10.10.1.0/24" ip_addr="10.10.1.2"
```

#### Add/List/Remove VRF:

```sh
st2 run phpipam.add_vrf name="TENANT1" rd="100:100" description="Core VRF" sections="Customers;IPv6"
```

```sh
st2 run phpipam.list_vrfs
```

```sh
st2 run phpipam.del_vrf name="TENANT1"
```

