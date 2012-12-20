import a10maltego, sys
from xml.dom.minidom import parseString

DEBUG = 0

def parseA10XML(xml):
    
    user_activity_lists = xml.getElementsByTagName("user_activity")
    
    userip = []
    starttime = []
    endtime = []
    hostname = []
    
    for user_activity_list in user_activity_lists:
        
        try:
            ip = user_activity_list.getElementsByTagName("user_ip")[0].firstChild.data
            userip.append(ip)
        except:
            userip.append("null")

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
        
    buildMaltegoXML(userip, starttime, endtime, hostname)

def buildMaltegoXML(user_ip, starttime, endtime, hostname):
    
    header="""<MaltegoMessage>
    <MaltegoTransformResponseMessage>
        <Entities>"""
        
    print header
    
    for idx, ip in enumerate(user_ip):
        print"""            <Entity Type='maltego.IPv4Address'>
                    <Value>%s</Value>""" %(ip)
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

user = sys.argv[1]

reqXML = a10maltego.a10xml("0", user, "False")

a10Response = a10maltego.a10request(reqXML)

dom = parseString(a10Response)

parseA10XML(dom)

if DEBUG:
    print "\nD: A10 Response-----\n" + a10Response + "\n-------"
