import logging
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, xsd
from zeep.transports import Transport
from creds import qb_credentials
import csv


class QBadapter:
    # When instantiating the class, open a session with Questback with suitable credentials
    def __init__(self):
        # Set uo log
        self.log = logging.getLogger('main_log')

        self.session = Session()
        self.session.auth = HTTPBasicAuth(qb_credentials.username, qb_credentials.password)
        self.client = Client("https://yf2810.customervoice360.com/service/?handler=soap&wsdl=1",
                             transport=Transport(session=self.session))
        self.log.info("New QBadapter created")

    # Method to get system time (for testing)
    def get_system_time(self):
        result = self.client.service.efs_system_getTime('D, d M Y H:i:s')
        print(result)

    # Method to get list of samples for a given survey Id
    def get_all_samples(self):
        result = self.client.service.survey_samples_getList(1394)
        print(result)
        pass

    def get_questions_base(self, surveyId):
        self.log.info("(Method get_questions_base). Accessing service to retrive questionnaire for survey %i" % surveyId)
        surveyId_type = self.client.get_type('ns0:survey_surveyId')

        result = self.client.service.survey_questionnaire_getStructure(surveyId=surveyId)

        return result["return"]

    def get_questions(self, surveyId):
        self.log.info("Querying EFS for questionnaire")
        questionnaire_raw = self.get_questions_base(surveyId)
        questionnaire = {}
        # DEVNOTE: THIS IS A JSON-LIKE REPOSNSE THAT NEEDS TO BE INTERPRETED
        for pages in questionnaire_raw:
            for page in pages:
                print (page)
                input("...")

    # Returns a CSV-formatted text string given a surveyId (integer)
    def get_results(self, surveyId):
        # surveyId_type = client.get_type('survey:surveyId')

        exportTypes_type = self.client.get_type('ns0:survey_surveyExportDataTypes')
        exportTypes = exportTypes_type(surveyExportDataType="QUESTIONNAIRE")

        rawDataExportConfig_type = self.client.get_type('ns0:survey_rawDataExportConfig')
        config = rawDataExportConfig_type(useCommaDelimiter="true",
                                          charset="UTF-8",
                                          exportTemplate="COMPLETE_SURVEY",
                                          missingValueNumeric="0")

        result = self.client.service.survey_results_getRawdataCSV(surveyId=surveyId,
                                                                  exportTypes=exportTypes,
                                                                  includeVariables=xsd.SkipValue,
                                                                  dateRange=xsd.SkipValue,
                                                                  sort=xsd.SkipValue,
                                                                  config=config)
        self.log.info("Queried for result of survey %s" % surveyId)
        # The actual data in the response is accessed with the key "return". It's in binary Base64 format
        answers_binary = result["return"]

        # Decode the binary data with utf-8 (as specified in charset above)
        answers_text = answers_binary.decode("utf-8")

        # Write a copy of the found answers to a csv file for better analysis readability (can be removed later)
        # self.writecopy(answers_text)

        # Note that this returns one long string with linefeed escape characters
        return answers_text

    def get_list_of_surveys(self):
        result = self.client.service.survey_surveys_getList()

        return result

    # Writes a variable to a file (expects text)
    @staticmethod
    def writecopy(text):
        with open("dump.csv", "w") as f:
            f.write(text)
        return True

    # Retrieves the latest survey result and returns it as a dict-like object
    def get_latest_result(self, surveyId):
        answers = self.get_results(surveyId)

        # Create a dictreader to access values more easily. Splitlines() method required to get fieldheaders attribute
        # function correctly
        answers_reader = csv.DictReader(answers.splitlines())

        # Iterate through all answers and store the "lfdn" value (index) in 'last_lfdn"
        for row in answers_reader:
            last_lfdn = row['lfdn']
        self.log.info("lfdn value of last line found as %s" % last_lfdn)

        # Reset reader (each DictReader can only be used once)
        answers_reader = csv.DictReader(answers.splitlines())

        # Find the last row and return that dict
        for row in answers_reader:
            if row['lfdn'] == last_lfdn:
                return row

        # In case of failure to find the last row, raise error
        raise IndexError("Failed to find latest result in method get_latest_result()")