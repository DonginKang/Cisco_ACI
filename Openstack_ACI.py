import os
import time
import requests
import novaclient.v2.client as nvclient
from neutronclient.v2_0 import client
from novaclient.client import Client
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from cobra.mit.request import ConfigRequest
from cobra.model.fv import RsBd, Ctx, BD, RsCtx, Subnet, Ap, Tenant, AEPg, RsCons, RsProv
from cobra.model.vz import Filter, Entry, BrCP, Subj, RsSubjFiltAtt


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


def get_nova_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d

def get_nova_credentials_v2():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d


def print_values(val, type):
    if type == 'ports':
        val_list = val['ports']
    if type == 'networks':
        val_list = val['networks']
    if type == 'routers':
        val_list = val['routers']
    for p in val_list:
        for k, v in p.items():
            print("%s : %s" % (k, v))
        print('\n')


def print_values_server(val, server_id, type):
    if type == 'ports':
        val_list = val['ports']

    if type == 'networks':
        val_list = val['networks']
    for p in val_list:
        bool = False
        for k, v in p.items():
            if k == 'device_id' and v == server_id:
                bool = True
        if bool:
            for k, v in p.items():
                print("%s : %s" % (k, v))
            print('\n')

			

# aci initialize 
			
session = LoginSession('https://IP', 'user',
                       'password')
moDir = MoDirectory(session)
moDir.login()

configReq = ConfigRequest()

uniMo = moDir.lookupByDn('uni')

fvTenantMo = Tenant(uniMo, 'admin')
fvApMo = Ap(fvTenantMo, 'sample_app')
fvCtxMo = Ctx(fvTenantMo, 'private-net')


### network 


network1_name = 'sample_network1'
credentials = get_credentials()
neutron = client.Client(**credentials)

try:
    body_sample = {'network': {'name': network1_name,
                   'admin_state_up': True}}

    netw = neutron.create_network(body=body_sample)
    net_dict = netw['network']
    network1_id = net_dict['id']
  

    body_create_subnet = {'subnets': [{'cidr': '192.168.100.0/24',
                          'ip_version': 4, 'network_id': network1_id}]}
	
    subnet = neutron.create_subnet(body=body_create_subnet)
    val_list = subnet['subnets']
    for p in val_list:
        for k, v in p.items():
	    if k=='id': subnet1_id = v 


finally:
    fvAEPgMoWeb1 = AEPg(fvApMo, 'sample_epg1')
    fvBDMo1 = BD(fvTenantMo, 'sample_bd1')
    fvSubnetMo = Subnet(fvBDMo1,ip='192.168.100.1/24')
    fvRsCtx = RsCtx(fvBDMo1, tnFvCtxName=fvCtxMo.name)
    fvRsBd1 = RsBd(fvAEPgMoWeb1, fvBDMo1.name)
    print("Network1 completed")
	

### network 2

network2_name = 'sample_network2'
credentials = get_credentials()
neutron = client.Client(**credentials)

try:
    body_sample = {'network': {'name': network2_name,
                   'admin_state_up': True}}

    netw = neutron.create_network(body=body_sample)
    net_dict = netw['network']
    network2_id = net_dict['id']


    body_create_subnet = {'subnets': [{'cidr': '192.168.200.0/24',
                          'ip_version': 4, 'network_id': network2_id}]}

    subnet = neutron.create_subnet(body=body_create_subnet)
    val_list = subnet['subnets']
    for p in val_list:
        for k, v in p.items():
	    if k=='id': subnet2_id = v 



finally:
	fvAEPgMoWeb2 = AEPg(fvApMo, 'sample_epg2')
	fvBDMo2 = BD(fvTenantMo, 'sample_bd2')
	fvSubnetMo = Subnet(fvBDMo2,ip='192.168.200.1/24')
	fvRsCtx = RsCtx(fvBDMo2, tnFvCtxName=fvCtxMo.name)
	fvRsBd2 = RsBd(fvAEPgMoWeb2, fvBDMo2.name)
        print("Network2 completed")




### server 1

try:
    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)

    image = nova_client.images.find(name="cirros")
    flavor = nova_client.flavors.find(name="m1.tiny")
    net = nova_client.networks.find(label=network1_name)
    nics = [{'net-id': net.id}]
    instance = nova_client.servers.create(name="gang_vmtest", image=image,
                                      flavor=flavor, key_name="osdev_key", nics=nics)
    instance = nova_client.servers.create(name="gang_vmtest2", image=image,
                                      flavor=flavor, key_name="osdev_key", nics=nics)
    #print("Sleeping for 5s after create command")
    time.sleep(2)

finally:
    print("Server1(Vm1,Vm2) Completed")

### server 2

try:
    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)

    image = nova_client.images.find(name="cirros")
    flavor = nova_client.flavors.find(name="m1.tiny")
    net = nova_client.networks.find(label=network2_name)
    nics = [{'net-id': net.id}]
    instance = nova_client.servers.create(name="gang_vmtest", image=image,
                                      flavor=flavor, key_name="osdev_key", nics=nics)
    instance = nova_client.servers.create(name="gang_vmtest2", image=image,
                                      flavor=flavor, key_name="osdev_key", nics=nics)
    #print("Sleeping for 5s after create command")
    time.sleep(2)
finally:
    print("Server2(Vm1,Vm2) Completed")



try:
    credentials = get_credentials()
    neutron = client.Client(**credentials)
    neutron.format = 'json'
    request = {'router': {'name': 'test_router',
                          'admin_state_up': True}}
    router = neutron.create_router(request)
    router_id = router['router']['id']
      
    body1 = { 'subnet_id' : subnet1_id }
    response = neutron.add_interface_router(router_id,body=body1)
   
   

    body2 = { 'subnet_id' : subnet2_id }
    response = neutron.add_interface_router(router_id,body=body2)




finally:
    filterMo = Filter(fvTenantMo, 'WebFilter')
    vzBrCPMoHTTP = BrCP(fvTenantMo, 'Contract')
    vzSubjMo = Subj(vzBrCPMoHTTP, 'WebSubject')
    fv_rscons = RsCons(fvAEPgMoWeb1,'Contract')
    fv_rscons = RsCons(fvAEPgMoWeb2,'Contract')
    fv_rscons = RsProv(fvAEPgMoWeb1,'Contract')
    fv_rscons = RsProv(fvAEPgMoWeb2,'Contract')
    RsSubjFiltAtt(vzSubjMo, tnVzFilterName=filterMo.name)
    configReq.addMo(fvTenantMo)
    moDir.commit(configReq)
    print("Router Completed")
    print("ACI Completed")
    print "Type delete : "
    


    a = raw_input()
    if a == 'delete':
        neutron.remove_interface_router(router_id,body=body1)
        neutron.remove_interface_router(router_id,body=body2)

        print ( " ---------------start removing all---------------" )

# remove all server 
        credentials = get_nova_credentials_v2()
        nova_client = Client(**credentials)


        servers_list = nova_client.servers.list()
        for s in servers_list:
            nova_client.servers.delete(s)


# remove all router

        credentials = get_credentials()
        neutron = client.Client(**credentials)
        routers_list = neutron.list_routers(retrieve_all=True)


        val_list = routers_list['routers']
        for p in val_list:
            for k, v in p.items():
                if k=='id': neutron.delete_router(v)



# remove all ports
		credentials = get_credentials()
		neutron = client.Client(**credentials)
		ports = neutron.list_ports()

		val_list = ports['ports']

        try:
            for p in val_list:
                for k, v in p.items():
                    if k=='id': neutron.delete_port(v)

# remove all networks

        finally:
            credentials = get_credentials()
            neutron = client.Client(**credentials)
            netw = neutron.list_networks()

            val_list = netw['networks']
            for p in val_list:
              	for k, v in p.items():
				    if k=='id': neutron.delete_network(v)

            #fvAEPgMoWeb1.delete()
            #fvAEPgMoWeb2.delete()
            #fvBDMo1.delete()
            #fvBDMo2.delete()
            #fvCtxMo.delete()
            #fvApMo.delete()
            fvTenantMo.delete()
            configReq.addMo(fvTenantMo)
            moDir.commit(configReq)

            print ( " -------------------completed -------------------" )
