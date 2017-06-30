import logging
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, xsd
from zeep.transports import Transport
import CREDENTIALS
import csv

logging.basicConfig(level=logging.INFO)


class QBadapter:

    # Method to get system time (for testing)
    def get_system_time(self):
        result = self.client.service.efs_system_getTime('D, d M Y H:i:s')
        print(result)

    # Method to get list of samples for a given survey Id
    def get_all_samples(self):
        result = self.client.service.survey_samples_getList(1394)
        print(result)
        pass

    # Method to get survey results as a CSV
    def get_results(self):
        # surveyId_type = client.get_type('survey:surveyId')

        exportTypes_type = self.client.get_type('ns0:survey_surveyExportDataTypes')
        exportTypes = exportTypes_type(surveyExportDataType="QUESTIONNAIRE")

        rawDataExportConfig_type = self.client.get_type('ns0:survey_rawDataExportConfig')
        config = rawDataExportConfig_type(useCommaDelimiter="true",
                                          charset="UTF-8",
                                          exportTemplate="COMPLETE_SURVEY")

        result = self.client.service.survey_results_getRawdataCSV(surveyId=1394,
                                                                  exportTypes=exportTypes,
                                                                  includeVariables=xsd.SkipValue,
                                                                  dateRange=xsd.SkipValue,
                                                                  sort=xsd.SkipValue,
                                                                  config=config)

        answers_binary = result["return"]
        answers_text = answers_binary.decode("utf-8")

        with open("OutputTest_b.txt", 'wb') as f1:
            f1.write(answers_binary)

        with open("OutputText_t.txt", "w") as f2:
            f2.write(answers_text)

        return answers_text

    def __init__(self):
        self.session = Session()
        self.session.auth = HTTPBasicAuth(CREDENTIALS.username, CREDENTIALS.password)
        self.client = Client("https://yf2810.customervoice360.com/service/?handler=soap&wsdl=1",
                             transport=Transport(session=self.session))

if __name__ == "__main__":
    qba = QBadapter()

    answers = qba.get_results()
    # dialect = csv.Dialect(delimiter=',')
    # csv.register_dialect("qbcsv", delimiter=",", doublequote=False)
    # answers_dict = csv.DictReader(answers, dialect="qbcsv")
    answers_dict = csv.DictReader(answers, dialect="unix")
    import code
    code.interact(local=locals())
