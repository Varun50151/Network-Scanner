from concurrent.futures import ThreadPoolExecutor
import socket
import nmap
from datetime import datetime
from colorama import Fore
from Email_sender import send_email

def hosts_avail():
    address=input("Enter the network address: ")
    nm=nmap.PortScanner()
    nm.scan(hosts=address,arguments="-sn")
    live_hosts=[]
    for host in nm.all_hosts():
        if nm[host].state()=="up":
            live_hosts.append(host)
            print(Fore.GREEN + f"Host found: {host} - {nm[host].hostname()}")
    return live_hosts

def single_port_scan(target,port):
    try: 
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result=sock.connect_ex((target,port))  
        sock.close()      
        if result==0:
            return port
    except:
        return None
    
def port_scan(target, start_port, end_port):
    print(f"Scanning target {target} for open ports from {start_port} to {end_port}....")
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(single_port_scan, target, port) 
                   for port in range(start_port, end_port + 1)]
        for future in futures:
            result = future.result()
            if result is not None:
                open_ports.append(result)
                print(Fore.GREEN + f"[+] Open port found: {result}")
    return sorted(open_ports)
    

def banner_grab(target, port):
    print(f"Grabbing banner for {target}:{port}")
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target,port))
        sock.settimeout(2)
        banner=sock.recv(1024).decode("utf-8",errors="ignore")
        sock.close()
        return banner.strip()
    except:
        return None

def vulnerability_scan(target):
    print(f'scanning target {target} for vulnerabilities')
    nm=nmap.PortScanner()
    try:
        nm.scan(hosts=target, arguments="-O -sV --script=vuln" )
        return nm[target]
    except Exception as e:
        print(f"Error during vulnerabiloty scan: {e}")

def network_scan(target, start_port,end_port):
    print(f'Starting network scan for target {target}')
    start_time=datetime.now()
    open_ports=port_scan(target, start_port, end_port)
    banners={}
    for port in open_ports:
        banner=banner_grab(target,port)
        banners[port]=banner if banner else "No banner found"
    
    vuln_info=vulnerability_scan(target)
    hostnames_rawinfo = vuln_info.get('hostnames', []) if vuln_info else []
    hostnames = ', '.join([h['name'] for h in hostnames_rawinfo if h['name']]) or "N/A"
    osmatch_raw = vuln_info.get('osmatch', []) if vuln_info else []
    if osmatch_raw:
        os_name = osmatch_raw[0]['name']
        os_accuracy = osmatch_raw[0]['accuracy']
        os_family = osmatch_raw[0]['osclass'][0]['osfamily'] if osmatch_raw[0].get('osclass') else 'N/A'
        os_info = f"{os_name} (Family: {os_family}, Accuracy: {os_accuracy}%)"
    else:
        os_info = "N/A"
    vulns = vuln_info.get('vulns', 'None detected') if vuln_info else 'None detected'
    
    end_time=datetime.now()
    scan_duration=end_time - start_time
    COMMON_PORTS = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        80: "HTTP", 135: "RPC", 139: "NetBIOS", 443: "HTTPS",
        445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt"
    }

    report = f"""
==========================================
       FULL NETWORK SCAN REPORT         
==========================================

  Target        : {target}
  Ports Scanned : {start_port} - {end_port}
  Scan Duration : {scan_duration}

******************************************
  OPEN PORTS
******************************************
"""
    if open_ports:
        for port in open_ports:
            service = COMMON_PORTS.get(port, "Unknown")
            report += f"  Port {port:<6} : {service}\n"
    else:
        report += "  No open ports found\n"

    report += f"""
******************************************
  BANNERS
******************************************
"""
    for port, banner in banners.items():
        report += f"  Port {port}: {banner}\n"

    report += f"""
******************************************
  SYSTEM INFO
******************************************
  Hostnames        : {hostnames}
  Operating System : {os_info}

******************************************
  VULNERABILITIES
******************************************
  {vulns if vulns else "No vulnerabilities detected"}

******************************************
  Scan completed at: {end_time.strftime("%Y-%m-%d %H:%M:%S")}
******************************************
"""
    print(report)
    return open_ports, report

if __name__=="__main__":
    email_id=input("Enter your email to receive reports: ")
    while True:
        print("1. Host Discovery")
        print("2. Port Scan")
        print("3. Full Network Scan")
        print("4. Exit")
        choice=int(input("Choose an option: "))
        if choice==1:
            live_hosts=hosts_avail()
            send_email(email_id, subject="Host Discovery Report",message=f"Live hosts found: {live_hosts}")
        elif choice==2:
            target_ip=input("Enter the IP address of the target: ")
            start_port=int(input("Enter the starting port for scanning: "))
            end_port=int(input("Enter the ending port for scanning: "))
            open_ports=port_scan(target_ip, start_port, end_port)
            send_email(email_id, subject="Port Scan Report",message=f"Open ports on {target_ip}: {open_ports}")
        elif choice==3:
            target_ip = input("Enter the IP address of the target: ")
            start_port = int(input("Enter the starting port for scanning: "))
            end_port = int(input("Enter the ending port for scanning: "))
            open_ports,report=network_scan(target_ip, start_port,end_port)
            send_email(email_id, subject="Full Network Scan Report",message=report)
        elif choice==4:
            print("Exiting")
            break
        else:
            print("Input a correct option")
    
