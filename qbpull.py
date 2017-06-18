import logging
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
import CREDENTIALS

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    session = Session()
    session.auth = HTTPBasicAuth(CREDENTIALS.username, CREDENTIALS.password)
    client = Client("https://yf2810.customervoice360.com/service/?handler=soap&wsdl=1",
                    transport=Transport(session=session))
    result = client.service.efs_system_getTime('D, d M Y H:i:s')
    print(result)

