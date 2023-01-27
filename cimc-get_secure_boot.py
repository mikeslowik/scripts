# get Cisco UCS server Secure Boot state for list of CIMC IP addresses and print to stdout

from imcsdk.imchandle import ImcHandle

CIMCUSR = "admin"
CIMCPWD = "CIMC_PASSWORD"
CIMCIP_LIST = [ '192.168.100.11', '192.168.100.12', '192.168.100.13' ]


def cimc_get_secure_boot(cimc_ip_list=CIMCIP_LIST, cimc_usr=CIMCUSR, cimc_pwd=CIMCPWD):
    data = []
    for cimc_ip in cimc_ip_list:
        print(f"[INFO] Connecting to CIMC {cimc_ip}")
        try:
            # Create a connection handle
            handle = ImcHandle(cimc_ip, cimc_usr, cimc_pwd)

            # Login to the server
            handle.login()
            print(f"[INFO] Connected to CIMC {cimc_ip}, gathering data...")

            try:
                mo = handle.query_dn('sys/rack-unit-1/boot-policy/boot-security')
                secure_boot = getattr(mo, 'secure_boot')
                data.append({'cimc_ip': cimc_ip, 'secure_boot': secure_boot})
            except Exception as e:
                print(f'[ERROR] Failed to get CIMC data: {str(e)}\n')
                data.append({'cimc_ip': cimc_ip, 'secure_boot': 'Error fetching data'})
                
            # Logout from the server
            handle.logout()
            print(f"[INFO] Finished and disconnected from CIMC {cimc_ip}.\n")
        except Exception as e:
            print(f'[ERROR] failed to login to CIMC {cimc_ip}: {str(e)}\n')
            data.append({'cimc_ip': cimc_ip, 'secure_boot': 'Error fetching data'})
    return data


if __name__ == "__main__":
    for host_entry in cimc_get_secure_boot():
        print(f"{host_entry['cimc_ip']}, Secure Boot: {host_entry['secure_boot']}")
