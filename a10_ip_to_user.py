'''
@author: libresec
'''

import a10maltego, sys
from xml.dom.minidom import parseString

def parseA10XML(xml):
    
    user_activity_lists = xml.getElementsByTagName("user_activity_list")
 
    usernames = []
    starttime = []
    endtime = []
    hostname = []

    for user_activity_list in user_activity_lists:
        
        try:
            un = user_activity_list.getElementsByTagName("username")[0].firstChild.data
            usernames.append(un)
        except:
            usernames.append("null")
  
        try:
            st = user_activity_list.getElementsByTagName("time_start")[0].firstChild.data
            starttime.append(st)
        except:
            starttime.append("null")
        
        try:
            et = user_activity_list.getElementsByTagName("time_end")[0].firstChild.data
            endtime.append(et)
        except:
            endtime.append("null")
        
        try:
            hn = user_activity_list.getElementsByTagName("user_hostname")[0].firstChild.data
            hostname.append(hn)
        except:
            hostname.append("null")
    
    buildMaltegoXML(usernames, starttime, endtime, hostname)

def buildMaltegoXML(usernames, starttime, endtime, hostname):
        
    if usernames == []:
        a10maltego.errors(2)
    
    else:
        
        header="""<MaltegoMessage>
        <MaltegoTransformResponseMessage>
            <Entities>"""
        
        print header
            
        for idx, un in enumerate(usernames):
            print"""            <Entity Type='Person'>
                        <Value>%s</Value>""" %(un)
            print"""                    <DisplayInformation>"""
            print"""                        <Label Name="Start Time" Type="text/plain">%s</Label>""" %(starttime[idx])
            print"""                        <Label Name="End Time" Type="text/plain">%s</Label>""" %(endtime[idx])
            print"""                        <Label Name="Hostname" Type="text/plain">%s</Label>""" % (hostname[idx])
            print"""                    </DisplayInformation>"""
            print"""           </Entity>""" 
                    
                
        footer="""        </Entities>
        </MaltegoTransformResponseMessage> 
    </MaltegoMessage>"""
    
        print footer

ip = sys.argv[1]

reqXML = a10maltego.a10xml(ip, "0", "False")

a10Response = a10maltego.a10request(reqXML)

dom = parseString(a10Response)

parseA10XML(dom)

