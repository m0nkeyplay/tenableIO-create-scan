# createScanIO.py
***create scans from a json without the GUI and all those clicks***

*usage* `python3 createScanIO.py`

****What does the script do?****
- Gather environment data helpful for creating a scan (admin privs needed for this data), can skip if user does not have the rights
- Use a provided JSON file template or create your own with the scan data to publish
- Incorporate pyTenable to create the scan
- Possible to create scans as other users with impersonation

Environment data and scan creation logs get dropped in the /logs folder

JSON templates are located in the /templates folder.  Included in the folder is a file with descriptions of common fields to write a nice JSON.  There are also all the fields and audit files needed to do Policy Compliance and Clould Infrastructure auditing. 

****Requirements****
- pyTenable - https://github.com/tenable/pyTenable
- Tenable IO access and secret key 
- Scan Creator permissions

*****Current Templates*****  Please contribute more!
- Basic Agent Vuln Scan
- Basic Over the Wire Vuln Scan
- Basic Over the Wire Vuln Scan - SSH Credentials
- AWS Three Tier Level 1 and Web Foundations L1

******notes:******      fill in the following variables as needed per environment

               ak              <-- Access Key
               sk              <-- Secret Key
               proxies         <-- If you use a proxy, set it here.
               iUser           <-- If you need to impersonate a user fill in username here
                                   and uncomment tio.users.impersonate(iUser) at the end of the script


*****Click to see it action*****
[![asciicast](https://asciinema.org/a/mll5DwNoYSEOvhBwIq8LBFg9o.svg)](https://asciinema.org/a/mll5DwNoYSEOvhBwIq8LBFg9o)
