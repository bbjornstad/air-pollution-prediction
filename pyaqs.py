"""
This file contains modules that can be used to fetch the data from the EPA's
Air Quality Services API. Defines a class that can be used to fetch the data and 
return it in an appropriate format.
"""

import requests
import json
import pandas as pd


class AQSFetcher:
    """
    This class defines a template for an object that can fetch EPA open
    air quality data. Has the following attributes:
    - email: the email for the associated account
    - key: the identification key for the associated account
    - api_url (optional): the base URL for the API

    Has the following methods:
    - get_cbsas: gets a dataframe of the Core Based Statistcal Area (a
      metropolitan area with a central urban center and connecting transport)
    - get_state_codes: gets a dataframe with the states and their associated
      codes.
    - get_counties_by_state: gets a dataframe with counties and their associated
      codes for a given state.
    - get_sites_by_county: gets a dataframe with measurement sites and their
      associated ids from a given state and county code
    - get_parameter_classes: gets a dataframe with classes of parameters
      (things that can be measured) and some descriptions
    - get_parameter_list_by_class: gets a dataframe with a list of parameters
      and their associated codes given a particular class of parameters
    - annual_data_by_cbsa: given a cbsa, list of parameters, and timeframe,
      gets the annual summary dataframe from the EPA website and returns it.
    - annual_data_by_site: given site identification and parameters, gets
      the annual summary dataframe and returns it
    - annual_data_by_county: given county identification and parameters, gets
      the annual summary dataframe and returns it.
    - annual_data_by_state: given a state id and parameters, gets the annual
      summary dataframe and returns it.
    """

    def __init__(self, email, key, api_url='https://aqs.epa.gov/data/api'):
        """
        The class constructor. Can take in an alternative URL
        """
        self.email = email
        self.key = key
        self.api_url = api_url
        self.stub = f'?email={self.email}&key={self.key}'

    def get_cbsas(self):
        """
        Gets a list of Core Based Statistical Areas as a dataframe
        """
        url = self.api_url + '/list/cbsas' + self.stub
        response = requests.get(url)
        try:
            assert response.status_code == requests.codes.ok
            json_data = json.loads(response.content)['Data']
            df = pd.DataFrame.from_records(json_data)
            df.rename(columns={'value_represented': 'cbsa_name'}, inplace=True)
            return df
        except AssertionError:
            print('Bad URL!')

    def get_state_codes(self):
        """
        Gets a list of states and their associated codes that can be used to
        construct additional queries.
        """
        url = self.api_url + '/list/states' + self.stub
        response = requests.get(url)
        try:
            assert response.status_code == requests.codes.ok

            json_data = json.loads(response.content)['Data']
            df = pd.DataFrame.from_records(json_data)
            df.rename(
                columns={'value_represented': 'state_name'}, inplace=True)
            return df

        except AssertionError:
            print('Bad URL!')

    def get_counties_by_state(self, state):
        """
        Gets a list of counties for the given state, and their associated
        county ids. Takes in a state id as an integer wrapped as a string.
        """
        url = self.api_url + '/list/countiesByState' + self.stub
        url += f'&state={state}'
        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok

            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            df.rename(
                columns={'value_represented': 'county_name'}, inplace=True)
            return df

        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')

    def get_sites_by_county(self, state, county):
        """
        Gets the ids of measurement sites by county. Takes in a state id and
        county id as wrapped string integers.
        """
        url = self.api_url + '/list/sitesByCounty' + self.stub
        url += f'&state={state}&county={county}'
        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok
            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            df.rename(columns={'value_represented': 'site_name'}, inplace=True)
            return df

        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')

    def get_parameter_classes(self):
        """
        Gets the possible classes of parameters
        """
        url = self.api_url + '/list/classes' + self.stub
        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok
        except AssertionError:
            print('Bad URL!')

        json_data = json.loads(response.content)['Data']
        df = pd.DataFrame.from_records(json_data)
        df.rename(columns={
            'code': 'class_name',
            'value_represented': 'class_description'},
            inplace=True)
        return df

    def get_parameter_list_by_class(self, _class):
        """
        Given a class name, gets the possible parameters and their associated
        codes as a dataframe.
        """
        url = self.api_url + '/list/parametersByClass' + self.stub
        url += f'&pc={_class}'

        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok

            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            df.rename(
                columns={'value_represented': 'parameter_description'},
                inplace=True)
            return df

        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')

    def annual_data_by_cbsa(self, cbsa_code, params, bdate, edate):
        """
        Searches for annual data by the CBSA. These are generally large regions
        Takes the following arguments as integers or wrapped string integers:
        - cbsa_code: code for the cbsa area
        - params: id for the specified readings
        - bdate, edate: beginning and end dates in YYYYMMDD format
        """
        search_params = '&param='
        for p in params:
            search_params += str(p)
            search_params += ','
        search_params = search_params[:-1]
        search_params += f'&bdate={bdate}&edate={edate}&cbsa={cbsa_code}'
        url = self.api_url + '/annualData/byCBSA' + self.stub + search_params

        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok
            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            return df

        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')

    def annual_data_by_site(self, state, county, site, params, bdate, edate):
        """
        Searches for annual data by measurement site.
        Takes in arguments as integers or wrapped string integers:
        - state: id of the state
        - county: id of the county
        - site: id of the measurement site
        - params: id of the desired type of measurement
        - bdate, edate: beginning and end dates of the measurement in YYYYMMDD
          format
        """
        search_params = '&param='
        for p in params:
            search_params += str(p)
            search_params += ','
        search_params = search_params[:-1]
        search_params += (
            f'&state={state}' +
            f'&county={county}' +
            f'&bdate={bdate}' +
            f'&edate={edate}' +
            f'&site={site}')
        url = self.api_url + '/annualData/bySite' + self.stub + search_params

        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok
            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            return df
        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')

    def annual_data_by_county(self, state, county, params, bdate, edate):
        """
        Gets the annual data by county. 
        Takes the following parameters as integers or wrapped string integers:
        - state: state id code
        - county: county code
        - param: ids of desired parameters to measure
        - bdate, edate: start and end dates in YYYYMMDD format
        """
        url = self.api_url + '/annualData/byCounty' + self.stub
        search_params = '&param='
        for p in params:
            search_params += str(p)
            search_params += ','
        search_params = search_params[:-1]
        search_params += (
            f'&state={state}' +
            f'&county={county}' +
            f'&bdate={bdate}' +
            f'&edate={edate}')
        url += search_params

        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok

            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            return df

        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')

    def annual_data_by_state(self, state, params, bdate, edate):
        """
        Gets the annual data by state.
        Takes the following parameters as integers or wrapped string integers:
        - state: state id code
        - param: ids of desired parameters to measure
        - bdate, edate: start and end dates in YYYYMMDD format
        """
        url = self.api_url + '/annualData/byState' + self.stub
        search_params = '&param='
        for p in params:
            search_params += str(p)
            search_params += ','
        search_params = search_params[:-1]
        search_params += (
            f'&state={state}' +
            f'&bdate={bdate}' +
            f'&edate={edate}')
        url += search_params

        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok

            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            return df

        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')

    def get_monitors_at_site(self, state, county, site, params, bdate, edate):
        """
        Gets information about the monitoring aparatus at a particular site.
        Takes the following arguments as integers or wrapped string integers:
        - state: id of the state
        - county: id of the county
        - site: id of the site
        - params: a list of parameter ids to search for
        - bdate, edate: start and end dates in YYYYMMDD format
        """
        search_params = '&param='
        for p in params:
            search_params += str(p)
            search_params += ','
        search_params = search_params[:-1]

        search_params += (
            f'&state={state}' +
            f'&county={county}' +
            f'&bdate={bdate}' +
            f'&edate={edate}' +
            f'&site={site}')

        url = self.api_url + '/monitors/bySite' + self.stub + search_params

        response = requests.get(url)

        try:
            assert response.status_code == requests.codes.ok
            jsn = json.loads(response.content)
            json_header = jsn['Header']
            json_data = jsn['Data']

            if json_header[0]['rows'] == 0:
                raise ValueError

            df = pd.DataFrame.from_records(json_data)
            return df

        except AssertionError:
            print('Bad URL!')
        except ValueError:
            print('No matching data could be found!')
