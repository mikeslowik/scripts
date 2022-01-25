from imcsdk.imchandle import ImcHandle

# set correct CIMC credentials and IP address
CIMCUSR = "admin"
CIMCPWD = "CIMC_PASSWORD"
CIMCIP = "10.10.10.10"

def cimc_check_startup_firmware():
    print(f"[INFO] Connecting to CIMC {CIMCIP}\n")

    try:
        # Create a connection handle
        handle = ImcHandle(CIMCIP, CIMCUSR, CIMCPWD)

        # Login to the server
        handle.login()
        print("[INFO] Connected to CIMC, running operations...")

        print('***** Checking Startup firmware version *****')
        mo_class = 'FirmwareBootUnit'
        mos = handle.query_classid(mo_class)
        for mo in mos:
            descr = getattr(mo, 'description')
            ver = getattr(mo, 'version')
            print('* {0:70} {1}'.format(descr, ver))    
    except Exception as e:
        print(str(e))

    # Logout from the server
    handle.logout()
    print("\n[INFO] Finished and disconnected from CIMC.")


if __name__ == "__main__":
    cimc_check_startup_firmware()
