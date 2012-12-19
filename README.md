a10Maltego
==========
These Maltego transforms can be used to query A10 Networks IDsentrie. 

a10Maltego.py 
----------------
Module that handles communications A10.

a10Maltego.conf
----------------
Configuration that holds A10 username, password, and server information.


Transforms
--------------------
maltego.IPv4Address (Entity)

	a10_ip_to_user.py

maltego.Person (Entity)

    a10_user_to_ip.py

Dependencies 
-------------
These transforms have been tested in Mac OSX using Python 2.7.
The only multiplatform dependency is Python 2.7.

Addtionally, Netwitness's REST API must be enabled, it is not enabled by default on some appliances. Check the docs!


Thanks
-----------------
Paterva (@Paterva)<br/>
@bostonlink -- Thanks for nwmaltego and a starting point!
