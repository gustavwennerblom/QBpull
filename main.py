import config
import csv
import logging
import sys
import os
from io import StringIO
from dbmanager import DatabaseManager
from qbpull import QBadapter
from logging.handlers import TimedRotatingFileHandler
from models import ConsultingServicesTouchpoint


# Logging setup - copied from GPPTOne, adjusted based on GPPT
script_directory = os.path.dirname(os.path.realpath(__file__))
log = logging.getLogger('main_log')
log.setLevel(logging.DEBUG)
ch_dev = logging.StreamHandler(sys.stdout)
ch_prod = TimedRotatingFileHandler(filename=os.path.join(script_directory, config.log_directory, config.log_filename),
                                   when='d', interval=1, backupCount=7)
ch_dev.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
ch_prod.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(ch_dev)
log.info("Main logger {} set up to log into directory {}".format(log.name, os.path.join(os.getcwd())))

# Instantiate database handler and Questback handler
db = DatabaseManager()
qb = QBadapter()


def move_results(touchpoint):
    """
    Fetches results data from a touchpoint in Questback and pushes it to the stage database
    :param touchpoint: The name of a touchpoint as a string. Must be present in the touchpoint_ids dict in config.py
    :return: Status code 200 (int) if successful
    """
    assert touchpoint in config.touchpoint_ids.keys()
    if config.touchpoint_ids[touchpoint] == 0:
        return NotImplementedError

    data = get_results(touchpoint)
    if touchpoint == 'consulting_services':
        status = post_results_consulting_services(data)
        return status
    elif touchpoint == 'bes':
        raise NotImplementedError
    elif touchpoint == 'sbp':
        raise NotImplementedError


def get_results(touchpoint):
    """
    Fetches survey results from a touchpoint
    :param touchpoint: The name of a touchpoint as a string. Must be present in the touchpoint_ids dict in config.py
    :return: A string with comma-separated values representing the survey answers
    """
    assert touchpoint in config.touchpoint_ids.keys()
    try:
        touchpoint_id = config.touchpoint_ids.get(touchpoint)
    except KeyError:
        log.error('Bad argument to function get_data')
        sys.exit(1)
    data = qb.get_results(touchpoint_id)
    return data


def post_results_consulting_services(data):
    """
    Pushes data to stage database
    :param data: A csv string
    :return: True if successful
    """
    assert isinstance(data, str)
    reader = csv.DictReader(StringIO(data), delimiter=',', quotechar='"')
    new_record_counter = 0
    for row in reader:
        # Check if the record exists, using lfdn as key
        lfdn_exists = db.session.query(ConsultingServicesTouchpoint).filter_by(lfdn=row['lfdn']).all()
        if not lfdn_exists:
            new_record = ConsultingServicesTouchpoint(lfdn=row.get('lfdn'),
                                                      project_number=row.get('bg_08'),
                                                      subproject_number=row.get('bg_54'),
                                                      client_name=row.get('bg_09'),
                                                      p_spec=row.get('bg_16'),
                                                      assignment_type=row.get('bg_18'),
                                                      business_area=row.get('bg_21'),
                                                      project_cc=row.get('bg_26'),
                                                      q1=row.get('NKI1'),
                                                      q2=row.get('NKI2'),
                                                      q3=row.get('v_12'),
                                                      q4=row.get('Trade_KPI'),
                                                      q5=row.get('NPS'),
                                                      q6=row.get('Improvements_text'),
                                                      agr_prepared=row.get('bg_22'),
                                                      agr_updated=row.get('bg_23'),
                                                      survey_date=row.get('bg_52'))
            db.session.add(new_record)
            new_record_counter += 1
            log.info('Record with lfdn={} queued for database insert'.format(row['lfdn']))
        else:
            log.debug('Got already existing record lfdn={0}, skipping insert'.format(row['lfdn']))
    if new_record_counter:
        db.session.commit()
        log.info('{0} new records commited to database')
    else:
        log.info('No new inserts in database')
    return 200


def post_results_bes(data):
    pass


def post_results_sbp(data):
    pass


def post_results_bio(data):
    pass


if __name__ == '__main__':
    log.info('Starting sequence')
    for tp in config.touchpoint_ids.keys():
        try:
            move_results(tp)
        except NotImplementedError:
            log.error('Touchpoint {0} not yet implemented')


