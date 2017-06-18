#!/usr/bin/env python

import os
import sys
import re

ssh_config = os.environ['HOME'] + '/.ssh/config'
key_location = os.environ['HOME'] + '/.ssh/ssh-keys/'

box_ip = sys.argv[1]

# r = '^10.\d+.\d+$'
r = '10\.\d+\.\d+'


def check_config_for_ip(box_ip):
    print("in check_config_for_new_ip")
    grep_config = os.popen('cat ' + ssh_config + ' | grep ' + box_ip)
    result = grep_config.read()
    if result:
        print("%s is already in config file." % str(box_ip))
        return True
    else:
        print("New entry")
        return False


class Entry(object):
    def __init__(self, box_ip):
        self.ip = box_ip
        self.user = self._get_user()
        self.pem_key = self._get_pem_key()
        self.proxy_bool = self._get_proxy_bool()
        self.bastion = self._get_bastion()

    def _get_user(self):
        user = raw_input("User: ")
        return user

    def _get_pem_key(self):
        pem_key = raw_input("Pem key name: ")
        return pem_key

    def _get_proxy_bool(self):
        proxy_bool = raw_input("Proxy through bastion? (y/n) ")
        if proxy_bool is "y":
            return True
        elif proxy_bool is "n":
            return False
        else:
            print("Invalid input")
            sys.exit(0)

    def _get_bastion(self):
        if self.proxy_bool:
            bastion = raw_input("Bastion IP: ")
            return bastion
        else:
            return None

    def append_to_config(self):
        config_to_add = "\n\nHost %s\n\tUser %s\n\tIdentityFile %s%s" % (str(self.ip), self.user, key_location, self.pem_key)
        if self.proxy_bool:
            hp = "%h:%p"
            config_to_add = config_to_add + "\n\tProxyCommand ssh -F %s -W %s %s" % (ssh_config, hp, self.bastion)
        with open(ssh_config, "a") as f:
            f.write(config_to_add)
            f.close()


# starting main program
if re.search(r, str(box_ip)):
    print("Possibly a valid IP")
    check = check_config_for_ip(box_ip)
    if check:
        sys.exit(0)
    else:
        print("Making a new entry")
        new_entry = Entry(box_ip)
        # new_entry = Entry(box_ip, user, bastion, pem_key)
        print("IP is %s" % new_entry.ip)
        print("User is %s" % new_entry.user)
        print("Pem key is %s" % new_entry.pem_key)
        print("Adding to %s" % ssh_config)
        new_entry.append_to_config()
else:
    print("Not valid IP")
    sys.exit(0)
