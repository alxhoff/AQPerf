import requests
import json
import pandas as pd
import pycurl
from io import BytesIO
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class v2_oauth_transport:
    api_token_url = "https://classic.warcraftlogs.com/oauth/token"
    api_url = "https://classic.warcraftlogs.com/api/v2/client"

    def __init__(self, client_id, client_secret):

        data = "grant_type=client_credentials"
        buffer = BytesIO()
        crl = pycurl.Curl()
        crl.setopt(pycurl.POST, 1)
        crl.setopt(pycurl.POSTFIELDS, data)
        crl.setopt(pycurl.URL, v2_oauth_transport.api_token_url)
        crl.setopt(pycurl.VERBOSE, 1)
        crl.setopt(pycurl.USERPWD, "{}:{}".format(client_id, client_secret))
        crl.setopt(pycurl.WRITEDATA, buffer)

        crl.perform()
        self.token = json.loads(buffer.getvalue())['access_token']

        auth_header = "Bearer {}".format(self.token)
        header = {"Authorization": auth_header}

        transport = RequestsHTTPTransport(url=self.api_url, headers=header)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def query(self, query):
        gql_query = gql(query)
        return self.client.execute(gql_query)
