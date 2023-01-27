# get Cisco UCS server hostname for list of CIMC IP addresses and print to stdout

from imcsdk.imchandle import ImcHandle

CIMCUSR = 'admin'
CIMCPWD = "CIMC_PASSWORD"
CIMCIP_LIST = [ '192.168.100.11', '192.168.100.12', '192.168.100.13' ]

def cimc_get_hostname_and_ip(cimc_ip_list=CIMCIP_LIST, cimc_usr=CIMCUSR, cimc_pwd=CIMCPWD):
    hostname_and_ip_list = []
    for cimc_ip in cimc_ip_list:
        print(f"[INFO] Connecting to CIMC {cimc_ip}")
        try:
            # Create a connection handle
            handle = ImcHandle(cimc_ip, cimc_usr, cimc_pwd)

            # Login to the server
            handle.login()
            print(f"[INFO] Connected to CIMC {cimc_ip}, gathering data...")

            try:
                mo = handle.query_classid("MgmtIf")
                hostname = getattr(mo[0], 'hostname')
                ip_addr = getattr(mo[0], 'ext_ip')
                hostname_and_ip_list.append({'hostname': hostname, 'ip_addr': ip_addr})
            except Exception as e:
                print(f'[ERROR] Failed to get CIMC data: {str(e)}')
                
            # Logout from the server
            handle.logout()
            print(f"[INFO] Finished and disconnected from CIMC {cimc_ip}.\n")
        except Exception as e:
            print(f'[ERROR] failed to login to CIMC {cimc_ip}: {str(e)}')
    return hostname_and_ip_list


if __name__ == '__main__':
    for host_entry in cimc_get_hostname_and_ip():
        print(f"{host_entry['hostname']}, CIMC IP {host_entry['ip_addr']}")
