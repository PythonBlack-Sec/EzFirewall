#!/usr/bin/env python
import sys, os, time, subprocess
"""Author: PythonBlack

This tool utilizes iptables for easily implementing a default drop policy for a host based firewall.
The rules are formated in a dictionary-list and can be added to and modified as needed."""
author = "\033[4mPython|Black\033[0m\033[91m"


flush = ["iptables -F","iptables -X","ipset -F","ipset -X"]

default_drop =  ["iptables -P INPUT DROP","iptables -P FORWARD DROP","iptables -P OUTPUT DROP"]

default_accept =  ["iptables -P INPUT ACCEPT","iptables -P FORWARD ACCEPT","iptables -P OUTPUT ACCEPT"]

rules = {
"web":["iptables -A INPUT -p tcp -m multiport --sports 80,443 -m state --state ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -m state --state NEW,ESTABLISHED -j ACCEPT"],

"dns-out":["iptables -A INPUT -p udp --sport 53 -m state --state ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p udp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT"],

"ssh":["iptables -A INPUT -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT"],

"ping":["iptables -A INPUT -p icmp -j ACCEPT","iptables -A OUTPUT -p icmp -j ACCEPT"],

"dhcp-out":["iptables -A INPUT -p udp --sport 68 -m state --state ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p udp --dport 67 -m state --state NEW,ESTABLISHED -j ACCEPT"],

"vpn":["iptables -A INPUT -p udp --sport 1194 -m state --state ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p udp --dport 1194 -m state --state NEW,ESTABLISHED -j ACCEPT"],

"local-process":["iptables -A INPUT -i lo -j ACCEPT","iptables -A OUTPUT -o lo -j ACCEPT"],

"Plex":["iptables -A INPUT -p tcp --dport 32400 -m state --state NEW,ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p tcp --sport 32400 -m state --state ESTABLISHED,RELATED -j ACCEPT"],

"Deluge":["iptables -A INPUT -p tcp --dport 8112 -m state --state NEW,ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p tcp --sport 8112 -m state --state ESTABLISHED -j ACCEPT","iptables -A INPUT -p udp --dport 6881:6891 -m state --state NEW,ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p udp --sport 6881:6891 -m state --state NEW,ESTABLISHED -j ACCEPT","iptables -A INPUT -p udp --dport 7871:7891 -m state --state ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p udp --sport 7871:7891 -m state --state NEW,ESTABLISHED -j ACCEPT"],

"client":["iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT","iptables -A INPUT -i lo -j ACCEPT","iptables -A INPUT -p icmp -j ACCEPT","iptables -A INPUT -m conntrack --ctstate INVALID -j DROP","iptables -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT"],

"samba":["iptables -A INPUT -p tcp --dport 445 -m state --state NEW,ESTABLISHED -j ACCEPT","iptables -A OUTPUT -p tcp --sport 445 -m state --state ESTABLISHED -j ACCEPT"]
}

req_rules = []

page = """_______________________________________________________________________________________________
|____|___|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|
|__|___|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|___|__|
|  |                                                                                       |  |
|__|              )         (      (      (                                (      (        |__|
|  |           ( /(         )\ )   )\ )   )\ )         (  (        (       )\ )   )\ )     |  |
|__|     (     )\())       (()/(  (()/(  (()/(   (     )\))(   '   )\     (()/(  (()/(     |__|
|  |     )\   ((_)\   ___   /(_))  /(_))  /(_))  )\   ((_)()\ ) ((((_)(    /(_))  /(_))    |  |
|__|    ((_)   _((_) |___| (_))_| (_))   (_))   ((_)  _(())\_)() )\ _ )\  (_))   (_))      |__|
|  |    | __| |_  /        | |_   |_ _|  | _ \  | __| \ \((_)/ / (_)_\(_) | |    | |       |  |
|__|    | _|   / /         | __|   | |   |   /  | _|   \ \/\/ /   / _ \   | |__  | |__     |__|
|  |    |___| /___|        |_|    |___|  |_|_\  |___|   \_/\_/   /_/ \_\  |____| |____|    |  |
|__|_______________________________________________________________________________________|__|
|____|___|____|____|____|____|____|____|____|____|____|____|____|____|____|___|{}|__|
|__|___|____|____|____|____|____|____|____|____|____|____|____|____|____|___|____|____|____|__|
""".format(author)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def q_rules():
    for i in range(len(sys.argv[1:]) + 1):
        if i == 0:
            pass
        else:
            req_rules.append(sys.argv[i])
    safe_check()

def safe_check():
    try:
        bak_yn = raw_input("Would you like to make a backup of current rules? Y/n ")
        if bak_yn == "y" or bak_yn == "Y":
            os.system("iptables-save > before-ez-firewall")
            print bcolors.WARNING + "File saved to: before-ez-firewall\n" + bcolors.ENDC
        elif bak_yn == "n":
            print ""
            pass
        else:
            print bcolor.WARNING + "Unexpected error, try again\n" + bcolor.ENDC
            safe_check()

        print "The corresponding iptable rules will be added in this order:"
        for rule in req_rules:
            print rule,
        c_rules = raw_input("\nIs this correct? Y/n ")
        if c_rules == "n":
            print bcolors.WARNING + "Run script again with correct order!" + bcolors.ENDC
            sys.exit()
        elif c_rules == "y" or c_rules == "Y":
            print bcolors.WARNING + "\nLast chance..." + bcolors.ENDC
            t = 6
            while t >= 2:
                print t - 1
                time.sleep(1)
                t = t - 1
            set_fw()
        else:
            print bcolor.WARNING + "Unexpected error, try again\n" + bcolor.ENDC
            safe_check()
    except KeyboardInterrupt:
        print ""
        og = os.popen('resize -s 24 80').read()
        sys.exit()

def set_fw():
    for rule in flush:
        os.system(rule)

    for rule in default_drop:
        os.system(rule)

    for protocol in req_rules:
        for k,v in rules.items():
            if k == protocol:
                for i in range(len(v)):
                    os.system(v[i])
    end_prog()

def def_accept():
    try:
        print bcolors.FAIL + page + bcolors.ENDC
        print bcolors.WARNING + "Are you sure you want to flush your firewall? Y/n " + bcolors.ENDC
        choice = raw_input("")
        if choice == "n":
            sys.exit()
        elif choice == "Y" or choice == "y":
            for rule in flush:
                os.system(rule)

            for rule in default_accept:
                os.system(rule)
            print bcolors.FAIL + page + bcolors.ENDC
            new_rules = os.popen('iptables -nvL').read()
            print bcolors.OKGREEN + str(new_rules) + bcolors.ENDC
            og = os.popen('resize -s 24 80').read()
        else:
            print bcolors.WARNING + "Unexpected value, try again.\n" + bcolors.ENDC
            restore_fw()
    except KeyboardInterrupt:
        print ""
        og = os.popen('resize -s 24 80').read()
        sys.exit()

def restore_fw():
    try:
        print bcolors.FAIL + page + bcolors.ENDC
        print bcolors.WARNING + "Are you sure you want to revert to your old firewall rules? Y/n " + bcolors.ENDC
        choice = raw_input("")
        if choice == "n":
            sys.exit()
        elif choice == "Y" or choice == "y":
            os.system("iptables-restore < before-ez-firewall")
            print bcolors.OKGREEN +"\nOld rules have been restored" + bcolors.ENDC
            sys.exit()
        else:
            print bcolors.WARNING + "Unexpected value, try again.\n" + bcolors.ENDC
            restore_fw()
    except KeyboardInterrupt:
        print ""
        og = os.popen('resize -s 24 80').read()
        sys.exit()

def usage():
    print bcolors.FAIL + page + bcolors.ENDC
    print "Available Rules:"
    for k,v in rules.items():
        print k + " |",
    print "\n\nAdditional options:\n-F, --flush      Clear firewall and implement default accept policy"
    print "-R, --resotre    Revert back to old firewall rules before using EZ-FIREWALL"
    print "\nExample: {} ssh web dns".format(sys.argv[0])

def end_prog():
    try:
        os.system("clear")
        print bcolors.FAIL + page + bcolors.ENDC
        new_rules = os.popen('iptables -nvL').read()
        print bcolors.OKGREEN + str(new_rules) + bcolors.ENDC
        time.sleep(10)
        og = os.popen('resize -s 24 80').read()
    except KeyboardInterrupt:
        print ""
        og = os.popen('resize -s 24 80').read()
        sys.exit()

def main():
    os.system("resize -s 55 95")
    os.system("clear")
    uid = os.getuid()
    if uid != 0:
        print bcolors.FAIL + page + bcolors.ENDC
        print bcolors.WARNING + "Script must be run with sudo privileges!" + bcolors.ENDC
    if uid == 0:
        if not len(sys.argv[1:]):
            usage()
            sys.exit()
        if len(sys.argv[1:]):
            if sys.argv[1] == "-F" or sys.argv[1] == "--flush":
                def_accept()
            elif sys.argv[1] == "-R" or sys.argv[1] == "--restore":
                restore_fw()
            else:
                print bcolors.FAIL + page + bcolors.ENDC
                q_rules()

main()
