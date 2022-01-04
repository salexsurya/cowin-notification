"""Main module to find appointment and notify users."""
import datetime
import time

import pandas as pd

from utils.api import API
from utils import utility


class COWIN():
    """Load data, check appointment and notify users."""
    WAIT_SEC = 300

    def __init__(self) -> None:
        """Load data, check appointment and notify users."""
        self._api = API()
        self._districts = utility.load_districts()

    def main(self) -> None:
        """Main function to check appointment and notify users."""
        # Appointment date
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        sdate = tomorrow.strftime("%d-%m-%Y")

        # Load user data
        users = pd.read_csv('waiting_list.csv')

        # Continuosly check for availability
        for index, user in users.iterrows():
            # Initialize user detail
            name = user.Name
            age = user.Age
            location = user.Place
            pincode = user.Pincode
            district_name = user.District
            state_name = user.State
            phone_numbers = str(user.PhoneNumber)     
            center_id = 1

            # Get data from API for given district
            appointment = pd.DataFrame()
            all_dist_in_state = self._districts[self._districts.state_name == state_name].district_id.tolist()
            for district_id in all_dist_in_state:
                appointment = appointment.append(self._api.get_appointment_by_district(district_id, sdate), ignore_index=False)
            appointment.to_csv('app.csv')
            # Filter appointment by age and availability by center, picode and district
            appointment = appointment.sort_values(by=['date']).reset_index(drop=True)
            available = (appointment.min_age_limit <= age) & (appointment.available_capacity>0)
            apt_center = appointment[(available) & (appointment.center_id==center_id)].reset_index(drop=True)
            apt_pin = appointment[(available) & (appointment.pincode==pincode)].reset_index(drop=True)
            apt_dist = appointment[(available) & (appointment.district_name==district_name)].reset_index(drop=True)
            apt_state = appointment[available].reset_index(drop=True)

            # Notify users on preferred center
            df = pd.DataFrame()
            if len(apt_center) > 0:
                df = apt_center.copy()
            # Notify users on preferred picode
            elif len(apt_pin) > 0:
                df = apt_pin.copy()
            # Notify users on preferred district
            elif len(apt_dist) > 0:
                df = apt_dist.copy()
            # Notify users on preferred state
            elif len(apt_state) > 0:
                df = apt_state.copy()

            # Notify users and update user status
            if len(df) > 0:
                # Notify users over SMS
                df['distance'] = df.apply(lambda row: utility.find_dist_between(f'{location}, {district_name}',
                                                                            f'{row.address}, {row.pincode}, {row.district_name}'), axis=1)
                df = df.sort_values(by=['distance', 'date']).reset_index(drop=True)
                message = f"Vaccine {df.at[0, 'vaccine']} available."
                message = message + f" Center: {df.at[0, 'center_name']}, pincode: {df.at[0, 'pincode']}, district: {df.at[0, 'district_name']}."
                message = message + f" Date: {df.at[0, 'date']}. Fee type: {df.at[0, 'fee_type']}. Make appointment immediately."
                utility.sms(phone_numbers, message)

                # Clear user from list
                users = users.drop(index)
                users.to_csv('waiting_list.csv', index=False)

                # Update complete list
                completed = pd.read_csv('completed_list.csv')
                completed = completed.append(user.to_frame().T, ignore_index=False)
                completed.to_csv('completed_list.csv', index=False)

            time.sleep(COWIN.WAIT_SEC)


if __name__ == "__main__":
    cowin = COWIN()
    cowin.main()
