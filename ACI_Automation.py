# -*- coding: utf-8 -*-

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest

def Create_Tenant():

    from cobra.mit.request import ConfigRequest
    configReq = ConfigRequest()
    from cobra.model.fv import Tenant
    uniMo = moDir.lookupByDn('uni')

    Tname = raw_input("Input Tenant 'name' : ")

    fvTenantMo = Tenant(uniMo, Tname)

    Apgatsu = int(raw_input("Input Application Profile 'number' "))
    
    for i in range(Apgatsu):
        from cobra.model.fv import Ap
        Apname = raw_input("Input Apllication profile 'name' : ")
        fvApMo = Ap(fvTenantMo,Apname)
        Epggatsu = int(raw_input("Input EPG 'number' "))

        for i in range(Epggatsu):
            from cobra.model.fv import AEPg
            epgname = raw_input("Input EPG 'name' : ")
            fvAEPgMoWeb = AEPg(fvApMo,epgname)

    Vrfgatsu = int(raw_input("Input Vrf 'number' "))  

    for i in range(Vrfgatsu):
        from cobra.model.fv import Ctx, BD, RsCtx
        vrfname = raw_input("Input Vrf 'name' : ")
        fvCtxMo = Ctx(fvTenantMo,vrfname)
        Bdgatsu = int(raw_input("Input Bridge Domain 'number' ")) 
        for i in range(Bdgatsu):
            from cobra.model.fv import Ctx, BD, RsCtx
            bdname = raw_input("Input Brige Domain 'name' : ")
            fvBDMo = BD(fvTenantMo,bdname)
            fvRsCtx = RsCtx(fvBDMo, tnFvCtxName=fvCtxMo.name)
    
    configReq.addMo(fvTenantMo)
    moDir.commit(configReq)


session = LoginSession('https://IP', 'USER',
                       'PASSWORD')
moDir = MoDirectory(session)
moDir.login()


Tenants = raw_input("Input Tenant 'number' ")
Tenants_Number = int(Tenants)


for Tenant in range(Tenants_Number):
    Create_Tenant()



