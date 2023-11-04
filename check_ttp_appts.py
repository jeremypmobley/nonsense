
# Script to print out next available TTP appointment at Chicago location

import requests


GOES_URL_FORMAT = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=500&locationId={0}&minimum=1"
CHICAGO_LOC_ID = 11981


def get_loc_appts(location_id):
    """
    Function to return the available appts for a given location_id
    """
    appointments = requests.get(
        GOES_URL_FORMAT.format(location_id), timeout=30
    ).json()

    return appointments


def print_appt_info(appts):
    """
    Function to print out info about next appointment
    """
    if len(appts) == 0:
        print('No appointments currently available. Try again later')
    else:
        next_appt_text = f"Next appointment on {appts[0]['startTimestamp'][0:10]} at {appts[0]['startTimestamp'][11:]}"
        print(next_appt_text)


def check_api_has_appts():
    """
    Function to check that the TTP schedulerapi is responding with open appointments for at least 1 location
    """
    appointments = requests.get(
        "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&minimum=1", timeout=30
    ).json()
    if len(appointments) > 0:
        print('API is working! TTP is responding with available appointments')
    else:
        print('API is NOT working! TTP API is NOT responding with available appointments. Try again later')


def main():
    """
    Main function to check for next appointment and print the results
    """
    check_api_has_appts()
    appointments = get_loc_appts(location_id=CHICAGO_LOC_ID)
    print_appt_info(appts=appointments)


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        raise err
