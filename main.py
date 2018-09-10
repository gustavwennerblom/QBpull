import config
import csv
import logging
import sys
import os
from io import StringIO
from dbmanager import DatabaseManager
from qbpull import QBadapter
from logging.handlers import TimedRotatingFileHandler
from models import ConsultingServicesTouchpoint, BESTouchpoint, BOPandConnectTouchpoint, \
    TrainingsTouchpoint, BusinessPromotionTouchpoint
from mailer import LogMailer

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
log.addHandler(ch_prod)
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
        log.error('Touchpoint {0} has no Questbacksurvey mapped in config.py'.format(touchpoint))
        return NotImplementedError

    data = get_results(touchpoint)
    if touchpoint == 'consulting_services':
        post_results_consulting_services(data)
    elif touchpoint == 'bes':
        post_results_bes(data)
    elif touchpoint == 'bopandconnect':
        post_results_bop_and_connect(data)
    elif touchpoint == 'trainings':
        post_results_trainings(data)
    elif touchpoint == 'business_promotion':
        post_results_business_promotion(data)
    else:
        log.warning('Touchpoint {0} has no configured method to post data to stage database'.format(touchpoint))


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
    data = qb.get_results(touchpoint_id)
    return data


def post_results_consulting_services(data):
    """
    Pushes consulting services touchpoint data to stage database
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
            log.info('Consulting Services record with lfdn={} queued for database insert'.format(row['lfdn']))
        else:
            log.debug('Got already existing record lfdn={0}, skipping insert'.format(row['lfdn']))
    if new_record_counter:
        db.session.commit()
        log.info('{0} new Consulting Services records commited to database'.format(new_record_counter))
    else:
        log.info('No new inserts in database')
    return 200


def post_results_bes(data):
    """
    Pushes BES touchpoint data to stage database
    :param data: A csv string
    :return: True if successful
    """
    assert isinstance(data, str)
    reader = csv.DictReader(StringIO(data), delimiter=',', quotechar='"')
    new_record_counter = 0
    for row in reader:
        # Check if the record exists, using lfdn as key
        lfdn_exists = db.session.query(BESTouchpoint).filter_by(lfdn=row['lfdn']).all()
        if not lfdn_exists:
            new_record = BESTouchpoint(lfdn=row.get('lfdn'),
                                       client_number=row.get('bg_12'),
                                       client_name=row.get('bg_13'),
                                       p_spec=row.get('bg_16'),
                                       business_area=row.get('bg_21'),
                                       handling_unit=row.get('bg_27'),
                                       q1=row.get('NKI1'),
                                       q2=row.get('NKI2'),
                                       q4=row.get('Trade_KPI'),
                                       q6=row.get('Improvements_text'),
                                       survey_date=row.get('bg_52'))
            db.session.add(new_record)
            new_record_counter += 1
            log.info('BES record with lfdn={} queued for database insert'.format(row['lfdn']))
        else:
            log.debug('Got already existing BES record lfdn={0}, skipping insert'.format(row['lfdn']))
    if new_record_counter:
        db.session.commit()
        log.info('{0} new BES records commited to database'.format(new_record_counter))
    else:
        log.info('No new inserts in database')
    return 200


def post_results_bop_and_connect(data):
    """
    Pushes BOP and Connect touchpoint data to stage database
    :param data: A csv string
    :return: void
    """
    assert isinstance(data, str)
    reader = csv.DictReader(StringIO(data), delimiter=',', quotechar='"')
    new_record_counter = 0
    for row in reader:
        # Check if the record exists, using lfdn as key
        lfdn_exists = db.session.query(BOPandConnectTouchpoint).filter_by(lfdn=row['lfdn']).all()
        if not lfdn_exists:
            new_record = BOPandConnectTouchpoint(lfdn=row.get('lfdn'),
                                                 project_number=row.get('bg_08'),
                                                 subproject_number=row.get('bg_54'),
                                                 client_number=row.get('bg_12'),
                                                 client_name=row.get('bg_13'),
                                                 p_spec=row.get('bg_16'),
                                                 assignment_type=row.get('bg_18'),
                                                 business_area=row.get('bg_21'),
                                                 project_cc=row.get('bg_26'),
                                                 q1=row.get('NKI1'),
                                                 q2=row.get('NKI2'),
                                                 q3=row.get('v_12'),
                                                 q4=row.get('Trade_KPI'),
                                                 q5=row.get('v_13'),
                                                 q6=row.get('NPS'),
                                                 q7=row.get('Improvements_text'),
                                                 agr_prepared=row.get('bg_22'),
                                                 agr_updated=row.get('bg_23'),
                                                 survey_date=row.get('bg_52'))
            db.session.add(new_record)
            new_record_counter += 1
            log.info('BOP/Connect record with lfdn={} queued for database insert'.format(row['lfdn']))
        else:
            log.debug('Got already existing BES record lfdn={0}, skipping insert'.format(row['lfdn']))
    if new_record_counter:
        db.session.commit()
        log.info('{0} new BOP/Connect records commited to database'.format(new_record_counter))
    else:
        log.info('No new inserts in database')
    return 200


def post_results_trainings(data):
    """
    Pushes Trainings touchpoint data to stage database
    :param data: A csv string
    :return: void
    """
    assert isinstance(data, str)
    reader = csv.DictReader(StringIO(data), delimiter=',', quotechar='"')
    new_record_counter = 0
    for row in reader:
        # Check if the record exists, using lfdn as key
        lfdn_exists = db.session.query(TrainingsTouchpoint).filter_by(lfdn=row['lfdn']).all()
        if not lfdn_exists:
            new_record = TrainingsTouchpoint(lfdn=row.get('lfdn'),
                                             project_number=row.get('bg_08'),
                                             subproject_number=row.get('bg_54'),
                                             client_number=row.get('bg_12'),
                                             client_name=row.get('bg_13'),
                                             p_spec=row.get('bg_16'),
                                             assignment_type=row.get('bg_18'),
                                             business_area=row.get('bg_21'),
                                             project_cc=row.get('bg_26'),
                                             q1=row.get('NKI1'),
                                             q2=row.get('NKI2'),
                                             q3=row.get('Trade_KPI'),
                                             q4=row.get('Improvements_text'),
                                             agr_prepared=row.get('bg_22'),
                                             agr_updated=row.get('bg_23'),
                                             survey_date=row.get('bg_52'))
            db.session.add(new_record)
            new_record_counter += 1
            log.info('Training record with lfdn={} queued for database insert'.format(row['lfdn']))
        else:
            log.debug('Got already existing Training record lfdn={0}, skipping insert'.format(row['lfdn']))
    if new_record_counter:
        db.session.commit()
        log.info('{0} new Training records commited to database'.format(new_record_counter))
    else:
        log.info('No new inserts in database')


def post_results_business_promotion(data):
    """
    Pushes Business Promotion touchpoint data to stage database
    :param data: A csv string
    :return: void
    """
    assert isinstance(data, str)
    reader = csv.DictReader(StringIO(data), delimiter=',', quotechar='"')
    new_record_counter = 0
    for row in reader:
        # Check if the record exists, using lfdn as key
        lfdn_exists = db.session.query(BusinessPromotionTouchpoint).filter_by(lfdn=row['lfdn']).all()
        if not lfdn_exists:
            new_record = BusinessPromotionTouchpoint(lfdn=row.get('lfdn'),
                                                     project_number=row.get('bg_08'),
                                                     client_number=row.get('bg_12'),
                                                     client_name=row.get('bg_13'),
                                                     p_spec=row.get('bg_16'),
                                                     assignment_type=row.get('bg_18'),
                                                     business_area=row.get('bg_21'),
                                                     project_cc=row.get('bg_26'),
                                                     q1=row.get('NKI1'),
                                                     q2=row.get('NKI2'),
                                                     q3=row.get('v_12'),
                                                     q4=row.get('Trade_KPI'),
                                                     q5=row.get('v_15'),
                                                     q6=row.get('v_13'),
                                                     q7=row.get('NPS'),
                                                     q8=row.get('Improvements_text'),
                                                     agr_prepared=row.get('bg_22'),
                                                     agr_updated=row.get('bg_23'),
                                                     survey_date=row.get('bg_52'))
            db.session.add(new_record)
            new_record_counter += 1
            log.info('Business Promotion record with lfdn={} queued for database insert'.format(row['lfdn']))
        else:
            log.debug('Got already existing Business Promotion record lfdn={0}, skipping insert'.format(row['lfdn']))
    if new_record_counter:
        db.session.commit()
        log.info('{0} new Business Promotion records commited to database'.format(new_record_counter))
    else:
        log.info('No new inserts in database')


if __name__ == '__main__':
    log.info('Starting sequence')

    # Iterate through all touchpoints (production mode)
    for tp in config.touchpoint_ids.keys():
        try:
            move_results(tp)
        except NotImplementedError:
            log.error('Touchpoint {0} not yet implemented'.format(tp))
    logmailer = LogMailer()
    logfile_pointer = os.path.abspath(os.path.join(os.getcwd(), config.log_directory, config.log_filename))
    logmailer.send_mail(subject_text="Log from QBpull",
                        body_text="Check attachment for log details",
                        attachment_path=logfile_pointer)
    log.info('All done. Log email distribution triggered')
