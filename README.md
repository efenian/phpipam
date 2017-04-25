Stackstorm pack for {php}IPAM
======


Here is what you need:

  - [Stackstorm](https://docs.stackstorm.com/install/index.html#installation)
  - [{php}IPAM 1.2](http://phpipam.net/documents/download-phpipam/) (you can try my [vagrant](https://github.com/efenian/phpipamvagrant) as well)

You will have to enable the phpipam API and have mod_rewrite working.

The phpipam API configuration should be placed in the phpipam.yaml file in the stackstom configuration directory.  I have only implimented the None and SSL API security methods, I have not yet implimented crypt support.  SSL method is recommended for encryption.

### Sample phpipam.yaml

```yaml
---
    api_uri: "https://192.168.16.30/api/app/"
    api_username: "admin"
    api_password: "password"
    api_verify_ssl: False
```

### Examples

#### Add/List/Remove device(s):

```sh
st2 run phpipam.add_device hostname="VDX-6740-RB1" ip_addr="198.18.0.1" devicetype="Switch" model="VDX-6740T" vendor="Brocade" sections="Customers;IPv6"
```

```sh
st2 run phpipam.list_devices
```

```sh
st2 run phpipam.del_device hostname="VDX-6740-RB1"
```

#### Add/List/Remove Layer 2 domain(s):

```sh
st2 run phpipam.add_l2domain name="dc1" description="my new datacenter"
```

```sh
st2 run phpipam.list_l2domains
```

```sh
st2 run phpipam.del_l2domain name="dc1"
```

#### Add/List/Remove VLAN(s):

```sh
st2 run phpipam.add_vlan name="tenant1" number="100" description="my new tenant vlan" l2domain="default"
```

```sh
st2 run phpipam.list_vlans
```

```sh
st2 run phpipam.del_vlan number="100" l2domain="default"
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
st2 run phpipam.list_subnets section="Customers"
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

This [patch](https://github.com/phpipam/phpipam/commit/c82f1e2f2c7f6f4fe85acbecaabd29d29cbd256b#diff-fc7a4e8b27a5f071cd6e8a7e405bda08) is required for device association to work.


```sh
st2 run phpipam.add_address section="Customers" subnet_cidr="10.10.1.0/24" ip_addr="10.10.1.1" hostname="TE-1/0/1.CoreSwitch" description="TE-1/0/1" is_gateway="0" tag="Used" mac="aa:bb:cc:dd:ee:f1" owner="infra" device="CoreSwitch" note="test"
```

```sh
st2 run phpipam.add_address section="Customers" subnet_cidr="10.10.1.0/24" ip_addr="10.10.1.2" hostname="TE-1/0/2.CoreSwitch" description="TE-1/0/2" is_gateway="0" tag="Used" mac="aa:bb:cc:dd:ee:f2" owner="infra" device="CoreSwitch" note="test
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
