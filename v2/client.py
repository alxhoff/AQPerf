from v2.transport import v2_oauth_transport

class Client:

    def __init__(self, client_id, client_secret):

        self.transport = v2_oauth_transport(client_id, client_secret)

    def get_rankings(self):
        query = """
            query {
                reportData { 
                    report(code:"C1dRfApW8Prm7kGX") {rankings}
                }
            }
            """

        result = self.transport.query(query)

        return result["reportData"]["report"]["rankings"]["data"]