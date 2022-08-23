from scraper.icbc import check_icbc
from datetime import datetime
from dateutil.parser import parse
from dotenv import dotenv_values

import time

config = dotenv_values(".env")

def main():
    my_appointment_date = datetime.strptime("12/13/2022", "%m/%d/%Y")
    start_time = time.time()

    date_res = None

    while not date_res:
        # False positive warnings coming from the type hinting of dotenv_values()
        date_res = check_icbc(config["ICBC_LOGIN_URL"], # type: ignore
                              config["LOGIN_NAME"],     # type: ignore
                              config["LOGIN_LICENSE_NUMBER"], # type: ignore
                              config["LOGIN_KEY_WORD"])       # type: ignore

    if date_res:
        date_res = parse(date_res)
    else: return

    print(time.time() - start_time)

    string_version = date_res.strftime('%m/%d/%Y')
    if date_res <= my_appointment_date:
        print(f"EARLIER DAY FOUND: {string_version}")
    else:
        print(f"The earliest is at {string_version}")

if __name__ == "__main__":
    main()
