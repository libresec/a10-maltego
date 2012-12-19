'''
Created on Dec 11, 2012

@author: libresec
'''
from xml.dom.minidom import Document, parseString
import httplib, sys

DEBUG = 0

def a10xml(ipIn, userIn, endIn): #potential args --> ip, id, timeframes

    doc = Document()
    user = userIn
    ip = ipIn
    
    #open config file to grab server, username, and password
    conf = open('a10maltego.conf', 'r')
    config = conf.readlines()
    conf.close()

    for line in config:

        try:

            if 'USERNAME' in line:
                usr_list = line.strip().split('=')
                a10usr = str(usr_list[1]).lstrip("'").rstrip("'")
    
            elif 'PASSWORD' in line:
                passwd_list = line.strip().split('=')
                a10pass = str(passwd_list[1]).lstrip("'").rstrip("'")

        except:

            return 'Authentication has failed to NW please check your netwitness.conf file'
    
    #Create root element <IDSentrieServiceReq>
    IDSentrieServiceReq = doc.createElement("IDSentrieServiceReq")
    doc.appendChild(IDSentrieServiceReq)
    
    #Create required element <partner_id>
    partner_id = doc.createElement("partner_id")
    IDSentrieServiceReq.appendChild(partner_id)
    partner_idText = doc.createTextNode(a10usr)
    partner_id.appendChild(partner_idText)
    
    #create required element <partner_passcode>
    partner_passcode = doc.createElement("partner_passcode")
    IDSentrieServiceReq.appendChild(partner_passcode)
    partner_passcodeText = doc.createTextNode(a10pass)
    partner_passcode.appendChild(partner_passcodeText)
    
    #Create required element <service>
    service = doc.createElement("service")
    service.setAttribute("name", "IDSentrieUser")
    #service.setAttribute("version", "1.1")
    IDSentrieServiceReq.appendChild(service)
    
    #Create required element <action> 
    action = doc.createElement("action")
    #Will expand to grab other actions from command line args as needed (DHCPAuthInfoPut, MacIPGet, Heartbeat)
    action.setAttribute("id", "0103") #Other option from API doc --> IPIDActivityGet
    service.appendChild(action)

    if (user != "0"):
        username = doc.createElement("username")
        action.appendChild(username)
        usernameText = doc.createTextNode(user)
        username.appendChild(usernameText)
    
    types = doc.createElement("type")
    action.appendChild(types)
    typesText = doc.createTextNode("latest")
    types.appendChild(typesText)

    #Create <return_attribute_list> to get host name
    returnAttrib = doc.createElement("return_attribute_list")
    action.appendChild(returnAttrib)
    
    #Create <user_hostname> and add to return attribute list
    user_hostname = doc.createElement("user_hostname")
    returnAttrib.appendChild(user_hostname)

    if (ip != "0"):
        user_ip = doc.createElement("user_ip")
        action.appendChild(user_ip)
        user_ipText = doc.createTextNode(ip)
        user_ip.appendChild(user_ipText)

    #print doc.toprettyxml(indent="\t", newl="\n")
    return doc.toxml("utf-8")

def a10request(reqIn):
    
    data = reqIn
    
#open config file to grab server
    conf = open('a10maltego.conf', 'r')
    config = conf.readlines()
    conf.close()

    for line in config:

        try:
            if 'A10SERVER' in line:
                conc_list = line.strip().split('=')
                a10svr = str(conc_list[1]).lstrip("'").rstrip("'")
        
        except:  
            return 'Authentication has failed to NW please check your netwitness.conf file'
    
    try:
        connection = httplib.HTTPSConnection(a10svr, timeout=60)
        connection.request("POST", "/xml/request", data)
        response = connection.getresponse()
        content = response.read()
        
        if DEBUG:
            print "--REQUEST--"
            out = parseString(data)
            print out.toprettyxml(indent='  ', encoding=None)
            print "--RESPONSE--"
            print content
        
        if len(content) != 0:
            return (content)
        else:
            print "Nothing returned."
            sys.exit(0)
           
    except:
        print a10svr
        print "Network connection is borked or A10 is not responding. 134"
        sys.exit(0)   
