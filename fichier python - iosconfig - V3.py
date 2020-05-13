#!/usr/bin/python
# -*- coding: utf-8 -*-
#author : MOINE Ludovic

#%%
###############################################
###Partie 0.1
###Tools for python
###############################################
import pdb #for debugger

###############################################
###Partie 0.2
###Jinja Initialisation
###############################################
import jinja2

#global variables for template
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))


'''
Pour l'instant on oublie port channel
'''
#%%
###############################################
###Partie 1
###Generator name(spine and leaf)
###Note : useful for two rooms
###############################################

#generator for hostname spine
def gen_spine(nb_spine):
    '''
    

    Parameters
    ----------
    nb_spine : integer
        DESCRIPTION.
        Number of spines

    Returns
    -------
    chain_number : list of string
        DESCRIPTION.
        List of hostname for network configuration

    '''
    chain_init = 'CPE-ADMspSM'
    chain_number = []    
    for i in range(0,int(nb_spine),1):
        if i+1 <= int(int(nb_spine)/2):    
            chain_number.append(chain_init+'1-0'+str(i+1))
        else :
            chain_number.append(chain_init+'2-0'+str(i+1))
    return chain_number  

#generator for hostname leaf
def gen_leaf(nb_leaf):
    '''
    

    Parameters
    ----------
    nb_leaf : integer
        DESCRIPTION.
        number of leafs

    Returns
    -------
    [chain_number,chain_OOB] =>
    chain_number : list of strings
    chain_OOB : list of strings
        DESCRIPTION.
        List of leafs' name for network configuration

    '''
    #initial variables
    chain_init_number = 'CPE-ADMIfMIX-SM'
    chain_number = []
    counter_leaf = 1
    counter_pod = 1
    
    
    for i in range(0,nb_leaf,1):
            chain_number.append(chain_init_number+str(counter_pod)+'-A'+str(counter_leaf))
            counter_leaf = counter_leaf+1
            
            if counter_leaf > 2:
                 counter_leaf = 1
                 counter_pod = counter_pod + 1
            
    return chain_number

# %%
###############################################
###Partie 2
###Generator of adress (spine and leaf)
###Note : the following fonctions migth be 
###useful for other projects
###############################################
def convert_binary_network(adress_list):
    '''
    

    Parameters
    ----------
    adress_list : string of the ip adress
        DESCRIPTION.
        Please right it as the following example : '10.10.10.0'
        (don't forget the ' and the . )
    Returns
    -------
    network_bin : string
        DESCRIPTION.
        Concatened format of the binary version of the ip adress
    '''
    
    #initial variable
    
    network=adress_list.split('.')
    network_bin=""
    
    #convert binaire    
    
    for i in range(0,len(network),1):
        network[i] = format(int(network[i]), 'b')
        if len(network[i]) != 8:
            for v in range(0,8-len(network[i]),1):
                network[i] = '0'+ network[i]
        network_bin = network_bin + network[i]
    
    return network_bin

def gen_cut_half(ip_adress_string,mask_origin):
    '''
    

    Parameters
    ----------
    ip_adress_string : string of the initial ip adress
        DESCRIPTION.
        String of the initial ip adress
    mask_origin : integer
        DESCRIPTION.
        Mask of the original ip adress

    Returns
    -------
    list_network : list of strings
        DESCRIPTION.
        List of the strings of the network ip adress after the split operation into two different networks
    '''
    #pdb.set_trace()
    
    
    #initial variable
    
    list_network=[]
    network_classic=[]
    mask_now = mask_origin
    network_string_copy = ip_adress_string
        
    #setting bit at the position of the new mask int network binary concatened format
    
    network_bin = convert_binary_network(network_string_copy)
    mask_now = mask_now + 1
    network_bin = network_bin[0:mask_now-1]+'1'+network_bin[mask_now:]
    
    for u in range(0,4,1):
        network_classic.append(str(int(network_bin[u*8:u*8+8],2)))
    
    link = "."
    link = link.join(network_classic)
    
    #setting the new adress into the list of networks
    
    list_network.append(network_string_copy+'/'+str(mask_now))
    list_network.append(link+'/'+str(mask_now))
        
        
    return list_network

def gen_adress_global(ip_adress_string,mask_origin,mask_wanted):
    '''
    

    Parameters
    ----------
    ip_adress_string : string
        DESCRIPTION.
        String of the initial ip adress
    mask_origin : integer
        DESCRIPTION.
        Mask of the original ip adress
    mask_wanted : integer
        DESCRIPTION.
        Mask wanted for the final ip adress

    Returns
    -------
    list_network : list of string
        DESCRIPTION.
        list of the network ip adress after the split operation

    '''
    
    #error test
    if mask_wanted < mask_origin:
        return -1
    
    #initial variable
    list_network = [ip_adress_string+'/'+str(mask_origin)]
    list_stockage = list_network
    list_tmp = []
    mask_now = mask_origin
    number_of_operation = mask_wanted - mask_origin
    
    #pdb.set_trace()
    
    #operation of splitage
    
    for i in range(0,number_of_operation,1):
        
        for j in range(0,len(list_stockage),1):
            
            list_tmp =  list_tmp + gen_cut_half(list_stockage[j].split('/')[0], mask_now)
        
        
        list_network = list_network + list_tmp
        list_stockage = list_tmp
        list_tmp = []
        mask_now = mask_now+1  
        
    return list_network[2**number_of_operation-1:]


    
    
# %%
###############################################
###Partie 3
###Distribution adress
###Setting hostnames
###############################################

###############################################
###Partie 3.1
###Definition of pod_calculator()
###############################################
    
def pod_calculator(list_of_leaf):
    '''
    

    Parameters
    ----------
    list_of_leaf : list of string
        DESCRIPTION.
        List of string
    Returns
    -------
    list_of_pod : list of string
        DESCRIPTION.
        List of string whose element are packed two-by-two

    '''
    
    #initial variable
    borne_sup = 2
    borne_inf = 0
    list_of_pod = []
    
    #leaf's couple
    for i in range (0,int(len(list_of_leaf)/2),1):
        list_of_pod.append(list_of_leaf[borne_inf:borne_sup])
        borne_inf = borne_inf + 2
        borne_sup = borne_sup + 2
    return list_of_pod

###############################################
###Partie 3.2
###Setting of values
###############################################

#creation of hostname for spine
nb_spine = 4
list_of_spine = gen_spine(nb_spine)

#creation of hostname for leaf
nb_leaf = 4
list_of_leaf = gen_leaf(nb_leaf)

#creation of the networks for spine (mask = /26)
    
adress_given = '10.1.200.0/23'
adress_given_ip_part = adress_given.split('/')[0]
adress_given_mask_part = int(adress_given.split('/')[1])
mask_wanted = 26

list_network_spine = gen_adress_global(adress_given_ip_part,adress_given_mask_part,mask_wanted)[:nb_spine]

#creation of the subnets for spines'networks (mask = /31)
list_subnet_spine = []
mask_spine = int(list_network_spine[0].split('/')[1])
mask_wanted = 31

for i in range(0,nb_spine,1):
    list_subnet_spine.append(gen_adress_global(list_network_spine[i],mask_spine,mask_wanted))
    
#definition of the AS_BGP
AS_BGP = 65000

#creation of ip adress for mgmt
list_mgmt = gen_adress_global('192.168.10.0',24,32)

for i in range(0,len(list_mgmt),1):
    list_mgmt[i]=list_mgmt[i].split('/')[0]+'/24'

#we delete the first and last adress
list_mgmt=list_mgmt[1:len(list_mgmt)-1]

#creation of the loopback list for leafs
list_of_loopback_leaf = gen_adress_global(adress_given, adress_given_mask_part, adress_given_mask_part+1)
list_of_loopback_leaf = gen_adress_global(list_of_loopback_leaf[1],adress_given_mask_part+1,29)
list_of_loopback_leaf_2 =[]
for i in range(0,len(list_of_loopback_leaf),1):
    list_of_loopback_leaf_2.append(gen_adress_global(list_of_loopback_leaf[i],29,32))


#%%
###############################################
###Partie 4
###Template
###############################################
    
###############################################
###Partie 4.1
###Definition of seek()
###############################################

def seek(list_of_list,name):
    '''
    

    Parameters
    ----------
    list_of_list : list of lists of strings
        DESCRIPTION.
        list of lists of strings where the name to seek is present
    name : string
        DESCRIPTION.
        name of the data to seek

    Returns
    -1 => name is not present in the list given
    i => indicate the number of the list inside the big list, that contains the name
    u => indicate the index of the name in the sub list
    -------
    None.

    '''

    for i in range(0,len(list_of_list),1):
        for u in range(0, len (list_of_list[i]),1):
            if name == list_of_list[i][u]: 
                return(i,u)
    return(-1)


###############################################
###Partie 4.2
###Template for ip configuration
###############################################

def template_creation_ip(list_of_leaf,list_of_spine,list_of_network_spine,list_of_network_leaf,list_mgmt,list_of_loopback_leaf,spine=False,leaf=False,num_of_spine=None,num_of_pod=None,num_of_leaf=None):
    '''
    

    Parameters
    ----------
    list_of_leaf : list of string
    DESCRIPTION.
    list of the sting name of the leafs
    
    list_of_spine : list of string
    DESCRIPTION.
    list of the string name of the spines
    
    list_of_network_spine : list of string
    DESCRIPTION.
    list of the string network of the spines
    
    please rigth the network as the following example :
        '10.10.10.0'
    
    list_of_network_leaf : list of string
    DESCRIPTION.
    list of the network of the leaf
    
    please rigth the network as the following example :
        '10.10.10.0'
        
    list_mgmt : list of string
    DESCRIPTION.
    list of network for the management
    
    list_of_loopback_leaf : list of string
    DESCRIPTION.
    list for the loopback 
    
    spine : boolean, optional
    DESCRIPTION. The default is False.
    Set True to select a spine
    
    leaf : TYPE, optional
    DESCRIPTION. The default is False.
    Set True to select a leaf
    
    num_of_spine : TYPE, optional
    DESCRIPTION. The default is None.
    number of the spine
    
    If there are 4 spines, then the number could be 1,2,3,4
    etc
    
    num_of_pod : TYPE, optional
    DESCRIPTION. The default is None.
    number of the pod
    
    If there are 4 leafs, then the number could be 1,2
    etc
    
    num_of_leaf : TYPE, optional
    DESCRIPTION. The default is None.
    number of the leaf of the pod
    
    It could be 1 or 2
    
    
    
    Returns
    -------
    None
    
    DESCRIPTION.
    Print the template (ip) associated to the device wanted

    '''
    
    #instanciate template
    template = template_env.get_template('iosconfig2.conf')
    
    #error test
    if spine == True and (num_of_spine == None or num_of_spine <= 0):
        return -1
    if leaf == True and (num_of_leaf == None or num_of_leaf<= 0 or num_of_leaf >2) and (num_of_pod == None or num_of_pod<=0 or num_of_pod > len(list_of_spine)):
        return -1
    
    #initial values
    config={}
    
    #pod calculation
    list_of_leaf_pod = pod_calculator(list_of_leaf)
    list_mgmt_copy = pod_calculator(list_mgmt)
    list_of_spine_sm = pod_calculator(list_of_spine)
       
    if leaf == True and spine == False:
        
        #importation of dictionnaries
        from dico_config import interface_lfnumber,interface_lfdescription,interface_lfpower,interface_lfswitchport,interface_lfchannel_ip,interface_lf2switchport
        
        #cut of the useless part of the network according to the number of the leaf
        if num_of_leaf%2!=0:
            list_of_network_spine = list_of_network_spine[::2]
            list_of_network_leaf = list_of_network_leaf[::2]
        else :
            list_of_network_spine = list_of_network_spine[1::2]
            list_of_network_leaf = list_of_network_leaf[1::2]
        
        counter_host = -1
        
        #modification of dictionnaries
        for i in range(len(interface_lfnumber),len(interface_lfnumber)-int(len(list_of_spine)/2),-1):
           
            interface_lfdescription[i]='vers '+list_of_spine[counter_host]+' [Eth1/'+str(num_of_pod)+']'
            interface_lfpower[i]='no shutdown'
            interface_lfswitchport[i]='no switchport'
            interface_lf2switchport[i]='mtu 9216'
            interface_lfchannel_ip[i] = 'ip address '+gen_adress_global(list_of_network_leaf[counter_host][num_of_pod-1].split('/')[0],31,32)[1].split('/')[0]+'/31'
                
            
            counter_host = counter_host -1
        
        ##creation of the dictionnaries of the interfaces
            
        #initial variables
        dic_tmp={'number':'','description':'','power':'','switchport':'','switchport_2':'','channel_ip':''}
        interfaces_dic=interface_lfnumber
        
        #association of the different dictionnaries in one 
        for i in range(1,len(interface_lfnumber)+1,1):
            dic_tmp['number']=interface_lfnumber[i]
            dic_tmp['description']=interface_lfdescription[i]
            dic_tmp['power']=interface_lfpower[i]
            dic_tmp['switchport']=interface_lfswitchport[i]
            dic_tmp['switchport_2']=interface_lf2switchport[i]
            dic_tmp['channel_ip']=interface_lfchannel_ip[i]
            
            interfaces_dic.update({i : dic_tmp})
            dic_tmp={'number':'','description':'','power':'','switchport':'','switchport_2':'','channel_ip':''}
        
            
        #creation of dictionnary for vlan/loopback
        list_for_vlan_loopback = list_of_loopback_leaf[num_of_pod-1]
        list_for_vlan_loopback_definition = list_for_vlan_loopback[3:len(list_for_vlan_loopback)]
        list_for_vlan_loopback_definition_new=[]
        if num_of_leaf%2 == 0:
            
            for i in range(0,4,1):
                if i%2 != 0:
                    list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback_definition[i])
            
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[1])
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[2])            
        else :
            
            for i in range(0,4,1):
                if i%2 == 0:
                    list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback_definition[i])
                        
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[0])
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[2])
            

        #generation of template
        
        #interface part
        config['hostname'] = list_of_leaf_pod[num_of_pod-1][num_of_leaf-1]
        config['ip_mgmt'] = list_mgmt_copy[int(len(list_of_spine)/2):][num_of_pod-1][num_of_leaf-1]
        config['spine_conf'] = 'fabric forwarding anycast-gateway-mac fab4.1c0a.fde8'
        config['default_route'] = list_mgmt[-1].split('/')[0]
        config['interfaces'] = interfaces_dic
        
        #vlan and loopback part
        config['leaf'] = 'one'
        config['ip_vlan_2'] = list_for_vlan_loopback_definition_new[2].split('/')[0]+'/31'
        config['ip_vlan_loopback_0'] = list_for_vlan_loopback_definition_new[1]
        config['ip_vlan_loopback_1'] = list_for_vlan_loopback_definition_new[0]
        config['ip_vlan_loopback_1_secondary'] = list_for_vlan_loopback_definition_new[3]
        
        #instanciate template
        template = template_env.get_template('iosconfig2.conf')
        
        text_file = open('./Render/config_ip', "w")
        text_file.write(template.render(config))
        text_file.close()
    
    if spine==True and leaf==False:
        
        #importation of dictionnaries
        from dico_config import interface_spnumber,interface_spdescription,interface_sppower,interface_spswitchport,interface_spchannel_ip,interface_sp2switchport

        
        #number ethernet calculation
        counter_host,index_of_spine = seek(list_of_spine_sm,list_of_spine[num_of_spine-1])
        number_ethernet = []
        indice=0
        
        
        for i in range(50,50-int(len(list_of_spine)/2),-1):
            number_ethernet.append(str(i))
            indice=indice+1
        
        number_ethernet.reverse()
         
        
        #modification of dictionnaries
        for i in range(1,len(list_of_leaf)+1,1):
           
            interface_spdescription[i]= list_of_leaf[i-1]+' [Eth1/'+str(number_ethernet[counter_host])+']'
            interface_sppower[i]='no shutdown'
            interface_spchannel_ip[i] = 'ip address '+list_of_network_leaf[num_of_spine-1][i-1]
       
                                                           
        #association of the dictionnaries in one
        for i in range(len(list_of_leaf)+1,len(interface_spnumber)-5,1):        
            
            interface_spchannel_ip[i] = 'ip address '+list_of_network_leaf[num_of_spine-1][i-1]
     
        for i in range(len(interface_spnumber)-5,len(interface_spnumber)-3,1):
            
            if num_of_spine%2 == 0 :
                num_of_attribution = 0
            else :
                num_of_attribution = 1
            
            interface_spdescription[i]= list_of_spine_sm[counter_host][num_of_attribution]+' [Eth1/'+interface_spnumber[i]+']'
            interface_spchannel_ip[i] = ''
            interface_sp2switchport[i]= 'channel-group 1 mode active'
            interface_sppower[i]='no shutdown'
            
        for i in range(len(interface_spnumber)-3,len(interface_spnumber)+1,1):
            
            interface_spdescription[i] = 'NotUsed (leaf ready)'
            interface_sppower[i] = 'shutdown'
            interface_spswitchport[i] = ''
            interface_sp2switchport[i]= ''
            interface_spchannel_ip[i] = ''
            
        #creation dico interfaces
            
        #initial variables
        dic_tmp={'number':'','description':'','power':'','switchport':'','switchport_2':'','channel_ip':''}
        interfaces_dic=interface_spnumber
        
        for i in range(1,len(interface_spnumber)+1,1):
            dic_tmp['number']=interface_spnumber[i]
            dic_tmp['description']=interface_spdescription[i]
            dic_tmp['power']=interface_sppower[i]
            dic_tmp['switchport']=interface_spswitchport[i]
            dic_tmp['switchport_2']=interface_sp2switchport[i]
            dic_tmp['channel_ip']=interface_spchannel_ip[i]
            
            interfaces_dic.update({i : dic_tmp})
            dic_tmp={'number':'','description':'','power':'','switchport':'','switchport_2':'','channel_ip':''}
        
            
        #creation of dictionnaries for loopback and channel
        network_adress_loopback_spine = []
        list_of_network_spine_sm = pod_calculator(list_of_network_spine)
        
        #generation of the couple of adress for channel1
        for i in range(0,len(list_of_spine_sm),1):
            network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-2].split('/')[0]+'/31')
            network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-1].split('/')[0]+'/31')
        
        #inversion index_of_spine
        if index_of_spine == 1:
            hostname_channel = 0
        else:
            hostname_channel = 1
        
        
        #generation of template
        config['hostname'] = list_of_spine[num_of_spine-1]
        config['ip_mgmt'] = list_mgmt[num_of_spine-1]
        config['spine_conf'] = 'fabric forwarding anycast-gateway-mac fab4.1c0a.fde8'
        config['default_route'] = list_mgmt[-1].split('/')[0]
        config['interfaces'] = interfaces_dic
        
        #loopback and channel part
        config['hostname_channel'] = list_of_spine_sm[counter_host][hostname_channel]
        config['ip_adress_channel_1'] = network_adress_loopback_spine[num_of_spine-1]
        config['ip_loopback_0'] = gen_adress_global(list_of_network_spine[num_of_spine-1], 26, 32)[-3]
        
        #instanciate template
        template = template_env.get_template('iosconfig2.conf')
        
        text_file = open('./Render/config_ip', "w")
        text_file.write(template.render(config))
        text_file.close()


###############################################
###Partie 4.3
###Template for UNDERLAY configuration
###############################################

       
def template_creation_underlay(list_of_leaf,list_of_spine,list_of_network_spine,list_of_network_leaf,list_of_loopback_leaf,spine=False,leaf=False,num_of_spine=None,num_of_pod=None,num_of_leaf=None):
    '''
    

    Parameters
    ----------
    list_of_leaf : list of string
    DESCRIPTION.
    list of the sting name of the leafs
    
    list_of_spine : list of string
    DESCRIPTION.
    list of the string name of the spines
    
    list_of_network_spine : list of string
    DESCRIPTION.
    list of the string network of the spines
    
    please rigth the network as the following example :
        '10.10.10.0'
    
    list_of_network_leaf : list of string
    DESCRIPTION.
    list of the network of the leaf
    
    please rigth the network as the following example :
        '10.10.10.0'
    
    list_of_loopback_leaf : list of string
    DESCRIPTION.
    list for the loopback 
    
    spine : boolean, optional
    DESCRIPTION. The default is False.
    Set True to select a spine
    
    leaf : TYPE, optional
    DESCRIPTION. The default is False.
    Set True to select a leaf
    
    num_of_spine : TYPE, optional
    DESCRIPTION. The default is None.
    number of the spine
    
    If there are 4 spines, then the number could be 1,2,3,4
    etc
    
    num_of_pod : TYPE, optional
    DESCRIPTION. The default is None.
    number of the pod
    
    If there are 4 leafs, then the number could be 1,2
    etc
    
    num_of_leaf : TYPE, optional
    DESCRIPTION. The default is None.
    number of the leaf of the pod
    
    It could be 1 or 2

    Returns
    -------
    TYPE
        DESCRIPTION.
        Print the template (undelay) associated to the device wanted
    '''
    
    #instanciate template
    template = template_env.get_template('iosconfigunderlay.conf')
    
    #error test
    if spine == True and (num_of_spine == None or num_of_spine <= 0):
        return -1
    if leaf == True and (num_of_leaf == None or num_of_leaf<= 0 or num_of_leaf >2) and (num_of_pod == None or num_of_pod<=0 or num_of_pod > len(list_of_spine)):
        return -1
    
    #initial values
    config={}
    
    #pod calculation
    list_of_leaf_pod = pod_calculator(list_of_leaf)
    list_of_spine_sm = pod_calculator(list_of_spine)
    
    if leaf == True and spine == False:
        
        #importation of dictionnaries
        from dico_config import interface_lfnumber
                
        #creation of dictionnary for loopback
        list_for_vlan_loopback = list_of_loopback_leaf[num_of_pod-1]
        list_for_vlan_loopback_definition = list_for_vlan_loopback[3:len(list_for_vlan_loopback)]
        list_for_vlan_loopback_definition_new=[]
        
        if num_of_leaf%2 == 0:
            
            for i in range(0,4,1):
                if i%2 != 0:
                    list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback_definition[i])
            
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[1])
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[2])            
        else :
            
            for i in range(0,4,1):
                if i%2 == 0:
                    list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback_definition[i])
                        
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[0])
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[2])
            
        loopback_0 = list_for_vlan_loopback_definition_new[1]
        
        #interfaces 49 and 50 dictionnary
        number_interface_leaf_underlay = {}
        for i in range(len(interface_lfnumber)-int(len(list_of_spine)/2)+1,len(interface_lfnumber)+1,1):
            number_interface_leaf_underlay[i] = i
        
        #generation of template
        config['leaf'] = 'one'
        config['loopback_0'] = loopback_0
        config['number'] = number_interface_leaf_underlay
        
        text_file = open('./Render/config_underlay', "w")
        text_file.write(template.render(config))
        text_file.close()
        
    if spine == True and leaf == False:
        
        #importation of dictionnaries
        from dico_config import interface_spnumber
        
        #creation of dictionnaries for loopback and channel
        network_adress_loopback_spine = []
        list_of_network_spine_sm = pod_calculator(list_of_network_spine)
        #generation of the couple of adress for channel1
        for i in range(0,len(list_of_spine_sm),1):
            network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-2].split('/')[0]+'/31')
            network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-1].split('/')[0]+'/31')
        
        loopback_0 = gen_adress_global(list_of_network_spine[num_of_spine-1], 26, 32)[-3]
        
        #creation of a dictionnary for interfaces 1 to 26
        number_interface_spine_underlay = {}
        for i in range(1,len(interface_spnumber)-5,1): 
             number_interface_spine_underlay[i] = i
             
        config['loopback_0'] = loopback_0
        config['number'] = number_interface_spine_underlay
        
        text_file = open('./Render/config_underlay', "w")
        text_file.write(template.render(config))
        text_file.close()

def template_creation_pim(list_of_spine, list_of_network_spine=None, leaf=False,spine=False):
    '''
    

    Parameters
    ----------
    list_of_network_spine : list of string
    DESCRIPTION.
    list of the string network of the spines
    
    spine : boolean, optional
    DESCRIPTION. The default is False.
    Set True to select a spine
    
    leaf : TYPE, optional
    DESCRIPTION. The default is False.
    Set True to select a leaf

    Returns
    -------
    TYPE
        DESCRIPTION.
        Print the template (pim) associated to the device wanted
    '''
    
    #instanciate template
    template = template_env.get_template('iosconfigpim.conf')
        
    #initial values
    config={}
    
    #pod calculation
    list_of_spine_sm = pod_calculator(list_of_spine)
    
    if leaf == True and spine == False:
        
        #importation of dictionnaries
        from dico_config import interface_lfnumber
        
        #interfaces 49 and 50 dictionnary
        number_interface_leaf_pim = {}
        for i in range(len(interface_lfnumber)-int(len(list_of_spine)/2)+1,len(interface_lfnumber)+1,1):
            number_interface_leaf_pim[i] = i
        
        #generation of template
        config['leaf'] = 'one'
        config['number'] = number_interface_leaf_pim
        
        text_file = open('./Render/config_pim', "w")
        text_file.write(template.render(config))
        text_file.close()
        
    if spine == True and leaf == False:
        
        #error test
        if list_of_network_spine == None:
            return -1
        
        #importation of dictionnaries
        from dico_config import interface_spnumber
        
        #creation of dictionnaries for loopback and channel
        network_adress_loopback_spine = []
        list_of_network_spine_sm = pod_calculator(list_of_network_spine)
        loopback_0_spine_dic ={}
        
        #for 4 spines, calculation of loopback 0
        for v in range(0,4,1):
                
            #generation of the couple of adress for channel1
            for i in range(0,len(list_of_spine_sm),1):
                network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-2].split('/')[0]+'/31')
                network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-1].split('/')[0]+'/31')
            
            loopback_0_spine_dic[v] = gen_adress_global(list_of_network_spine[v], 26, 32)[-3]
        
        #creation of a dictionnary for interfaces 1 to 26
        number_interface_spine_pim = {}
        for i in range(1,len(interface_spnumber)-5,1): 
             number_interface_spine_pim[i] = i
        
        config['loopback_0'] = loopback_0_spine_dic
        config['number'] = number_interface_spine_pim
       
        text_file = open('./Render/config_pim', "w")
        text_file.write(template.render(config))
        text_file.close()

def template_creation_bgp(adress_given,list_of_spine,AS_BGP,list_of_network_spine,list_of_loopback_leaf,num_of_leaf= None,num_of_pod=None,num_of_spine=None,leaf=False,spine=False):
    '''
    

    Parameters
    ----------
    adress_given : string
        DESCRIPTION.
        global adress of the network
    list_of_spine : list of string
        DESCRIPTION.
        list of spine
    AS_BGP : integer
        DESCRIPTION.
        AS_BGP
    list_of_network_spine : list of string
        DESCRIPTION.
        list of network spine
    list_of_loopback_leaf : list of string
        DESCRIPTION.
        list of loopback for the leafs
    num_of_leaf : integer, optional
        DESCRIPTION. The default is None.
    num_of_pod : integer, optional
        DESCRIPTION. The default is None.
    num_of_spine : integer, optional
        DESCRIPTION. The default is None.
    leaf : boolean, optional
        DESCRIPTION. The default is False.
    spine : boolean, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    #instanciate template
    template = template_env.get_template('iosconfigbgp.conf')
            
    #error test
    if spine == True and (num_of_spine == None or num_of_spine <= 0):
        return -1
    if leaf == True and (num_of_leaf == None or num_of_leaf<= 0 or num_of_leaf >2) and (num_of_pod == None or num_of_pod<=0 or num_of_pod > len(list_of_spine)):
        return -1
    
    #initial values
    config={}
    
    #pod calculation
    list_of_spine_sm = pod_calculator(list_of_spine)
    
    if leaf == True and spine == False:
        
        #importation of dictionnaries
        from dico_config import interface_spnumber
        
        #creation of dictionnaries for loopback 
        network_adress_loopback_spine = []
        list_of_network_spine_sm = pod_calculator(list_of_network_spine)
        loopback_0_spine_dic ={}
        
        #for 4 spines, calculation of loopback 0
        for v in range(0,4,1):
                
            for i in range(0,len(list_of_spine_sm),1):
                network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-2].split('/')[0]+'/31')
                network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-1].split('/')[0]+'/31')
            
            loopback_0_spine_dic[v] = gen_adress_global(list_of_network_spine[v], 26, 32)[-3]
        
        #creation of dictionnary for loopback
        list_for_vlan_loopback = list_of_loopback_leaf[num_of_pod-1]
        list_for_vlan_loopback_definition = list_for_vlan_loopback[3:len(list_for_vlan_loopback)]
        list_for_vlan_loopback_definition_new=[]
        
        if num_of_leaf%2 == 0:
            
            for i in range(0,4,1):
                if i%2 != 0:
                    list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback_definition[i])
            
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[1])
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[2])            
        else :
            
            for i in range(0,4,1):
                if i%2 == 0:
                    list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback_definition[i])
                        
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[0])
            list_for_vlan_loopback_definition_new.append(list_for_vlan_loopback[2])
         
        loopback_0 = list_for_vlan_loopback_definition_new[1]
        
        #instantiation of the dictionnary for ospf
        dic_ospf={}
        
        for i in range(0,len(list_of_spine),1):
            dic_ospf[i]=''
        
        #association of string name spine with loopback in a dictionnary
        dic_tmp={'loopback':'','spine':''}
        
        for i in range(0,len(list_of_spine),1):
            dic_tmp['loopback']=loopback_0_spine_dic[i]
            dic_tmp['spine']=list_of_spine[i]
            
            dic_ospf.update({i : dic_tmp})
            dic_tmp={'loopback':'','spine':''}
        
        #generate template
        config['leaf'] = 'one'
        config['interfaces'] = dic_ospf
        config['as_bgp'] = str(AS_BGP)
        config['loopback_0'] = loopback_0
            
        text_file = open('./Render/config_bgp', "w")
        text_file.write(template.render(config))
        text_file.close() 
        
    if spine == True and leaf == False:
            
        #importation of dictionnaries
        from dico_config import interface_spnumber
        
        #creation of dictionnaries for loopback
        network_adress_loopback_spine = []
        list_of_network_spine_sm = pod_calculator(list_of_network_spine)
        
        for i in range(0,len(list_of_spine_sm),1):
            network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-2].split('/')[0]+'/31')
            network_adress_loopback_spine.append(gen_adress_global(list_of_network_spine_sm[i][0], 26, 32)[-1].split('/')[0]+'/31')
        
        loopback_0 = gen_adress_global(list_of_network_spine[num_of_spine-1], 26, 32)[-3]
        
        #generate template
        config['loopback_0'] = loopback_0
        config['as_bgp'] = str(AS_BGP)
        config['adress_given'] = adress_given
        
        text_file = open('./Render/config_bgp', "w")
        text_file.write(template.render(config))
        text_file.close()

# %%       
###############################################
###Partie 5
###Results
###############################################
        
###############################################
'''
Notice française :
    Manipuler les valeurs leaf = True ou spine = True pour sélectionner l'équipement
    Pour les leafs :
        manipuler num_of_pod pour choisir le pod
        manipuler num_of_leaf pour prendre le premier ou second leaf d'un pod
    Pour les spines :
        manipuler num_of_spine pour choisir le premier,... ou quatrième spine

Les implementations sont présentes ci-dessous
Les résultats sont dans le fichier "Render"
'''
        
template_creation_ip(list_of_leaf, list_of_spine, list_network_spine, list_subnet_spine, list_mgmt, list_of_loopback_leaf_2, spine=True, num_of_leaf=2, num_of_pod=1, num_of_spine=2)
template_creation_underlay(list_of_leaf, list_of_spine, list_network_spine, list_subnet_spine, list_of_loopback_leaf_2, spine=True, num_of_leaf=2, num_of_pod=1, num_of_spine = 2)
template_creation_pim(list_of_spine,list_network_spine,spine=True)
template_creation_bgp(adress_given,list_of_spine, AS_BGP, list_network_spine, list_of_loopback_leaf_2, num_of_leaf=2, num_of_pod=1, spine=True, num_of_spine = 2)
