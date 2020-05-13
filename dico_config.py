# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:58:52 2020

@author: Ludovic
"""


############################################
###Partie 0.0
###Dictionnary for interfaces leaf
############################################

interface_lfnumber={}
interface_lfdescription={}  
interface_lfpower={} 
interface_lfswitchport={}
interface_lf2switchport={}
interface_lfchannel_ip={}

############################################
###Partie 0.1
###Leafs'calculations
############################################

for i in range(1,51,1):
    interface_lfnumber[i]=str(i)
    interface_lfdescription[i]= 'NotUsed (VPC enabled)'
    interface_lfpower[i] = 'shutdown'
    interface_lfswitchport[i] = 'switchport mode trunk'
    interface_lf2switchport[i]= 'switchport trunk allowed vlan none'
    interface_lfchannel_ip[i] = 'channel-group '+str(100+i)+' mode active'
    
############################################
###Partie 1.0
###Dictionnary for interfaces spine
############################################
    
interface_spnumber={}
interface_spdescription={}  
interface_sppower={} 
interface_spswitchport={}
interface_sp2switchport={}
interface_spchannel_ip={}

############################################
###Partie 1.1
###Leafs'calculations
############################################

for i in range(1,33,1):
    interface_spnumber[i]=str(i)
    interface_spdescription[i]= 'NotUsed (leaf ready)'
    interface_sppower[i] = 'shutdown'
    interface_spswitchport[i] = 'mtu 9216'
    interface_sp2switchport[i]= 'no ip redirects'
    interface_spchannel_ip[i] = 'to define'
    
    
    
