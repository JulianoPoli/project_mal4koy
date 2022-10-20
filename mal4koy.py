import sys
import os
from datetime import datetime
import csv

auto_version = "v0.1.1"

def run_recon(target):
    time = datetime.now()
    dirname = f'{target}_{time.strftime("%d%m%Y%H%M%S")}'

    #create dirs
    os.system(f'mkdir report/{dirname}')
    os.system(f'mkdir report/{dirname}/subdomains') 
    os.system(f'mkdir report/{dirname}/ports')
    os.system(f'mkdir report/{dirname}/vulns')
    os.system(f'mkdir report/{dirname}/vulns/nuclei')

    #Domain enum
    os.system(f'subfinder -d {target} -o report/{dirname}/subdomains/subfinder.txt')
    with open(f"report/{dirname}/subdomains/subfinder.txt", 'a') as arquivo:
        print(target,file=arquivo)
    arquivo.close()
    
    #Port scan
    arq_domain = open(f"report/{dirname}/subdomains/subfinder.txt")
    lines = arq_domain.readlines()
    for subs in lines:
        os.system(f'python3 FireScan.py {subs.strip()} report/{dirname}/ports/')
    os.system(f'cat report/{dirname}/ports/open_ports_* > report/{dirname}/ports/all_open_ports.csv')
    os.system(f'rm report/{dirname}/ports/open_ports_*')

    #Active Domains
    with open(f'report/{dirname}/ports/all_open_ports.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            os.system(f'echo "{row[0]}" >>report/{dirname}/subdomains/active_domains_temp.txt')
    csv_file.close()
    os.system(f'uniq report/{dirname}/subdomains/active_domains_temp.txt >report/{dirname}/subdomains/active_domains.txt')
    os.system(f'rm report/{dirname}/subdomains/active_domains_temp.txt')


    #Vuln scan
    #Nuclei
    active_domains_arqv = open(f"report/{dirname}/subdomains/active_domains.txt")
    lines = active_domains_arqv.readlines()
    for line in lines:
        os.system(f'nuclei -u https://{line.strip()} -o report/{dirname}/vulns/nuclei/{line.strip()}.txt')


def help_menu():
    print(f"\nMal4koy {auto_version} - By JulianoPoli")
    print(f"\nBASIC COMMANDS")
    print(f"$ python3 mal4koy.py -t target.com")
    print(f"\nPARAMS")
    print(f"-t, --target        Set target URL in format target.com")
    print(f"-h, --help          Help options")
    print('\n')

if len(sys.argv) == 1:
    help_menu()
    exit()
elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    help_menu()
    exit()

for params in sys.argv:
    if params == "-t" or params == "--target":
        target_locate = sys.argv.index(params) + 1
        run_recon(sys.argv[target_locate])


