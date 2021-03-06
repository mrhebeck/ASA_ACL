#!/usr/bin/env python

# *------------------------------------------------------------------
# * Cisco ASA API Script
# * Author: Keith O'Brien
# * kobrien@cisco.com
# *
# * You must have an ASA setup with the REST API
# *
# *------------------------------------------------------------------
#

try:

    import requests
    import json
    import sys
    import logging
    from requests.auth import HTTPBasicAuth
    from pprint import pprint
    from optparse import OptionParser
    from getpass import getpass
    
except ImportError, error:
    sys.stdout.write('ImportError: %s \n' % error)
    sys.exit(1)

parser = OptionParser()
parser.add_option('-f', '--file', help="CSV Data File")
opts, args = parser.parse_args()

#if not opts.file: parser.error('File name is required')


if len(sys.argv) > 1:
    username = sys.argv[1]

if len(sys.argv) > 2:
    ip_address = sys.argv[2]

if len(sys.argv) > 3:
    acl_enable = sys.argv[3]

if len(sys.argv) == 1:
    print "Usage: acl_enable [username] [fw ip address] [allow or deny]"
    sys.exit(1)

password = getpass('Enter API Password for ASA:')

# JSON data that has to be sent to the ASA to enable and disable the ACL.

api_data_false = """{
    "sourceAddress": {
        "kind": "objectRef#NetworkObj",
        "refLink": "https://%s/api/objects/networkobjects/Filtered_Network",
        "objectId": "Filtered_Network"
    },
    "destinationAddress": {
        "kind": "AnyIPAddress",
        "value": "any4"
    },
    "destinationService": {
        "kind": "NetworkProtocol",
        "value": "ip"
    },
    "active": false
}""" % ip_address

api_data_true = """{
    "sourceAddress": {
        "kind": "objectRef#NetworkObj",
        "refLink": "https://%s/api/objects/networkobjects/Filtered_Network",
        "objectId": "Filtered_Network"
    },
    "destinationAddress": {
        "kind": "AnyIPAddress",
        "value": "any4"
    },
    "destinationService": {
        "kind": "NetworkProtocol",
        "value": "ip"
    },
    "active": true
}""" % ip_address


# Disables the certificate warning generated by the requests library
logging.captureWarnings(True)

firewall = 'https://%s' % ip_address
api_header = {'Content-Type': 'application/json'}

# 'Filtered' is the name of the ASA interface to which the acl is being applied
api_path = "https://%s/api/access/in/Filtered/rules" % ip_address

r = requests.get(api_path, auth=HTTPBasicAuth(username, password), headers=api_header,verify=False)
result_json = r.json()
try:
    decoded = json.loads(result_json)
    print decoded
    
except (ValueError, KeyError, TypeError):
    print "JSON format error"

pprint(result_json[u'items:'][u"objectId:"])


# The number at the end can change and should be retrieved first
api_path_object = "https://%s/api/access/in/Filtered/rules/1417028242" % ip_address
url = firewall + api_path


if __name__ == '__main__':


    if acl_enable == 'allow':
        r = requests.put(api_path_object, data = api_data_true, auth=HTTPBasicAuth(username, password), headers=api_header,verify=False)
    else:
        r = requests.put(api_path_object, data = api_data_false, auth=HTTPBasicAuth(username, password), headers=api_header,verify=False)


    if r.status_code == 204:
        print "Success -- Change completed"
    else:
        print "Failure -- Change failed"

  