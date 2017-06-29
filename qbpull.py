import logging
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, xsd
from zeep.transports import Transport
import CREDENTIALS

logging.basicConfig(level=logging.INFO)


def getSystemTime():
    pass

def getAllSamples():
    pass

if __name__ == "__main__":
    session = Session()
    session.auth = HTTPBasicAuth(CREDENTIALS.username, CREDENTIALS.password)
    client = Client("https://yf2810.customervoice360.com/service/?handler=soap&wsdl=1",
                    transport=Transport(session=session))

    ### Query procedure to get system time (for testing)
    # result = client.service.efs_system_getTime('D, d M Y H:i:s')
    # print(result)

    ### Query procedure to get list of samples for a given survey Id
    # result = client.service.survey_samples_getList(1394)
    # print(result)

    ### Query procedure to get information about a sample given a sample Id
    # result = client.service.survey_samples_get(1395)
    # print (result)

    ### Query procedure to get survey results as a CSV
    #surveyId_type = client.get_type('survey:surveyId')

    exportTypes_type = client.get_type('ns0:survey_surveyExportDataTypes')
    exportTypes = exportTypes_type(surveyExportDataType="QUESTIONNAIRE")

    rawDataExportConfig_type = client.get_type('ns0:survey_rawDataExportConfig')



    result = client.service.survey_results_getRawdataCSV(surveyId=1394,
                                                         exportTypes=exportTypes,
                                                         includeVariables=xsd.SkipValue,
                                                         dateRange=xsd.SkipValue,
                                                         sort=xsd.SkipValue,
                                                         config=xsd.SkipValue)

    with open("OutputTest.txt",'wb') as f:
        f.write(result["return"])


    print(result)