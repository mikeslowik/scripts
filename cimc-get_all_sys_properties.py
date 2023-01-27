# get all 'sys' properties for Cisco UCS server and save to file in OUT_DIR

from imcsdk.imchandle import ImcHandle
from os import getcwd, path
from time import time

CIMCUSR = "admin"
CIMCPWD = "CIMC_PASSWORD"
CIMCIP_LIST = [ '192.168.100.11', '192.168.100.12', '192.168.100.13' ]
OUT_DIR = path.dirname(getcwd())


def cimc_get_all_sys_properties(cimc_ip_list=CIMCIP_LIST, cimc_usr=CIMCUSR, cimc_pwd=CIMCPWD, out_dir=OUT_DIR):
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
                # for general / initial full output - all BIOS settings (MOs + attriputes/properties)
                mo_list = handle.query_dn("sys/rack-unit-1/bios/fw-boot-def/bootunit-combined",hierarchy=True)

                out_file_path = f'{out_dir}/{cimc_ip}_{str(time())}'
                with open(out_file_path, 'w+') as output:
                    print(f'[INFO] Saving output to file: {out_file_path}')
                    for mo in mo_list:
                        output.write(str(mo))

            except Exception as e:
                print(f'[ERROR] Failed to get CIMC data: {str(e)}\n')
                data.append({'cimc_ip': cimc_ip, 'secure_boot': f'Error fetching data: {str(e)}'})

            # Logout from the server
            handle.logout()
            print(f"[INFO] Finished and disconnected from CIMC {cimc_ip}.\n")
        except Exception as e:
            print(f'[ERROR] failed to login to CIMC {cimc_ip}: {str(e)}\n')
            data.append({'cimc_ip': cimc_ip, 'secure_boot': 'Error fetching data'})
    return data


if __name__ == "__main__":
    cimc_get_all_sys_properties()
