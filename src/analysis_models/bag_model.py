from src.data_manager import DataManager
import pandas as pd


class BagModel:

    def __init__(self, dm: DataManager = DataManager()):
        self.dm = dm

    def get_missing_bags(self):
        df = pd.read_csv("../../data/dbo_00000.V_NTNU_Export.csv", index_col=None, low_memory=False, header=0)

        df_filter = df[(df["bagTagNumber"] == 81757582)]
        with pd.option_context('display.max_rows', 20, 'display.max_columns', None):  # more options can be specified also
            print(df_filter)

        pass


"""
sourceOrganization,sourceSystem,sourceTimestamp,bagTagNumber,bagEventCode,bagEventTimestamp,bagEventAirportIATA,
bagEventLocation,bagEventDescription,bagEventErrorCode,bagFinalAirportIATA,LegArrayLength,
Leg0_departureAirportIATA,Leg0_arrivalAirportIATA,Leg0_operatingAirlineIATA,Leg0_flightId,Leg0_sobt,
Leg1_departureAirportIATA,Leg1_arrivalAirportIATA,Leg1_operatingAirlineIATA,Leg1_flightId,Leg1_sobt,
Leg2_departureAirportIATA,Leg2_arrivalAirportIATA,Leg2_operatingAirlineIATA,Leg2_flightId,Leg2_sobt,
Leg3_departureAirportIATA,Leg3_arrivalAirportIATA,Leg3_operatingAirlineIATA,Leg3_flightId,Leg3_sobt,
Leg4_departureAirportIATA,Leg4_arrivalAirportIATA,Leg4_operatingAirlineIATA,Leg4_flightId,Leg4_sobt,
Leg5_departureAirportIATA,Leg5_arrivalAirportIATA,Leg5_operatingAirlineIATA,Leg5_flightId,Leg5_sobt,
Leg6_departureAirportIATA,Leg6_arrivalAirportIATA,Leg6_operatingAirlineIATA,Leg6_flightId,Leg6_sobt,
Leg7_departureAirportIATA,Leg7_arrivalAirportIATA,Leg7_operatingAirlineIATA,Leg7_flightId,Leg7_sobt,
bagpnrcode
"""


hello = BagModel()
hello.get_missing_bags()