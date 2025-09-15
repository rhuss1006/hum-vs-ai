"""
Human vs. AI
api.py - api to configurate backend and frontend applications
Name: Rayd Hussain

5/23/2025
"""

import pandas as pd

class RECIPAPI:

    # Dataframe that contains the csv data
    recipients = None

    def load_recip(self, filename):
        """ Loads CSV File --> Converts into Dataframe
            filename - csv file containing recipient data"""

        self.recipients = pd.read_csv(filename)

    def get_state_data(self):
        """
        Get recipient count by state

        Returns:
        pandas.DataFrame: State-level data with recipient counts
        """

        return self.recipients['State Name'].value_counts().reset_index()

    def get_city_data(self):
        """
        Get recipient count by city/town and state

        Returns:
        pandas.DataFrame: City-level data with recipient counts
        """

        return self.recipients.groupby(
            ['Recipient/Sub-Recipient City', 'State Name']).size().reset_index(
            name='recipient_count')

    def get_city_coordinates(self):
        """
        Get city data with coordinates for mapping

        Returns:
        pandas.DataFrame: City data with lat/lon coordinates
        """

        coords_data = self.recipients[
            (self.recipients[
                 'Geocoding Artifact Address Primary X Coordinate'].notna()) &
            (self.recipients[
                 'Geocoding Artifact Address Primary Y Coordinate'].notna())
            ][['Recipient/Sub-Recipient City', 'State Name',
               'Common State Abbreviation',
               'Geocoding Artifact Address Primary X Coordinate',
               'Geocoding Artifact Address Primary Y Coordinate']]

        coords_data.columns = ['city_name', 'state_name', 'state_abbr',
                               'longitude', 'latitude']

        return coords_data

