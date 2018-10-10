from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class ConsultingServicesTouchpoint(Base):
    __tablename__ = 'ConsultingServicesTouchPoint'
    idx = Column(Integer, primary_key=True)
    lfdn = Column(Integer, unique=True)         # lfdn
    project_number = Column(Integer)            # bg_08 / m_cgi_project
    subproject_number = Column(String(15))        # bg_54 / m_cgi_subproject
    client_number = Column(Integer)             # bg_12 / m_cgi_customer
    client_name = Column(String(200))           # bg_13 (corrected) / m_cgi_customer_t
    p_spec = Column(Integer)                    # bg_16 / m_cgi_pspec
    assignment_type = Column(String(20))        # bg_18 / m_cgi_assignmenttyp
    business_area = Column(String(50))          # bg_21 / m_cgi_bus_unit_t
    project_cc = Column(Integer)                # bg_26 / m_cgi_costc
    q1 = Column(Integer)                        # NKI1
    q2 = Column(Integer)                        # NKI2
    q3 = Column(Integer)                        # v_12
    q4 = Column(Integer)                        # Trade_KPI
    q5 = Column(Integer)                        # NPS
    q6 = Column(String(3000))                   # Improvements_text
    agr_prepared = Column(DateTime)             # bg_22 / m_cgi_prepared
    agr_updated = Column(DateTime)              # bg_23 / m_cgi_updated
    survey_date = Column(DateTime)              # bg_52 / m_cg_exp_survey_date


class MISTouchpoint(Base):
    __tablename__ = 'MISTouchpoint'
    idx = Column(Integer, primary_key=True)
    lfdn = Column(Integer, unique=True)         # lfdn
    project_number = Column(Integer)            # bg_08 / m_cgi_project
    subproject_number = Column(String(15))      # bg_54 / m_cgi_subproject
    client_number = Column(Integer)             # bg_12 / m_cgi_customer
    client_name = Column(String(200))           # bg_13 / m_cgi_customer_t
    p_spec = Column(Integer)                    # bg_16 / m_cgi_pspec
    assignment_type = Column(String(20))        # bg_18 / m_cgi_assignmenttyp
    business_area = Column(String(50))          # bg_21 / m_cgi_bus_unit_t
    project_cc = Column(Integer)                # bg_26 / m_cgi_costc
    NKI1 = Column(Integer)                      # NKI1
    NKI2 = Column(Integer)                      # NKI2
    TradeKPI = Column(Integer)                  # Trade_KPI
    ImprovementsText = Column(String(3000))     # Improvements_text
    agr_prepared = Column(DateTime)             # bg_22 / m_cgi_prepared
    agr_updated = Column(DateTime)              # bg_23 / m_cgi_updated
    survey_date = Column(DateTime)              # bg_52 / m_cg_exp_survey_date


class BESTouchpoint(Base):
    __tablename__ = 'BESTouchpoint'
    idx = Column(Integer, primary_key=True)
    lfdn = Column(Integer, unique=True)         # lfdn
    client_number = Column(Integer)         # bg_12 !!!
    client_name = Column(String(200))           # bg_13 !!!
    p_spec = Column(Integer)                    # bg_16
    business_area = Column(String(50))          # bg_21
    project_cc = Column(Integer)                # void
    handling_unit = Column(String(100))         # bg_27
    q1 = Column(Integer)                        # NKI1
    q2 = Column(Integer)                        # NKI2
    q4 = Column(Integer)                        # Trade_KPI
    q6 = Column(String(3000))                   # Improvements_text
    survey_date = Column(DateTime)              # bg_52


class BOPandConnectTouchpoint(Base):
    __tablename__ = 'BOPandConnectTouchpoint'
    idx = Column(Integer, primary_key=True)
    lfdn = Column(Integer, unique=True)         # lfdn
    project_number = Column(Integer)            # bg_08
    subproject_number = Column(String(15))      # bg_54
    client_number = Column(Integer)             # bg_12
    client_name = Column(String(200))           # bg_13
    p_spec = Column(Integer)                    # bg_16
    assignment_type = Column(String(20))        # bg_18
    business_area = Column(String(50))          # bg_21
    project_cc = Column(Integer)                # bg_26
    q1 = Column(Integer)                        # NKI1
    q2 = Column(Integer)                        # NKI2
    q3 = Column(Integer)                        # v_12
    q4 = Column(Integer)                        # Trade_KPI
    q5 = Column(Integer)                        # v_13
    q6 = Column(Integer)                        # NPS
    q7 = Column(String(3000))                   # Improvements_text
    agr_prepared = Column(DateTime)             # bg_22
    agr_updated = Column(DateTime)              # bg_23
    survey_date = Column(DateTime)              # bg_52


class TrainingsTouchpoint(Base):
    __tablename__ = 'TrainingsTouchpoint'
    idx = Column(Integer, primary_key=True)
    lfdn = Column(Integer, unique=True)         # lfdn
    project_number = Column(Integer)            # bg_08
    subproject_number = Column(String(15))      # bg_54
    client_number = Column(Integer)             # bg_12
    client_name = Column(String(200))           # bg_13
    p_spec = Column(Integer)                    # bg_16
    assignment_type = Column(String(20))        # bg_18
    business_area = Column(String(50))          # bg_21
    project_cc = Column(Integer)                # bg_26
    q1 = Column(Integer)                        # NKI1
    q2 = Column(Integer)                        # NKI2
    q3 = Column(Integer)                        # Trade_KPI
    q4 = Column(String(3000))                   # Improvements_text
    agr_prepared = Column(DateTime)             # bg_22
    agr_updated = Column(DateTime)              # bg_23
    survey_date = Column(DateTime)              # bg_52


class BusinessPromotionTouchpoint(Base):
    __tablename__ = 'BusinessPromotionTouchpoint'
    idx = Column(Integer, primary_key=True)
    lfdn = Column(Integer, unique=True)     # lfdn
    project_number = Column(Integer)        # bg_08
    subproject_number = Column(String(15))  # ?
    client_number = Column(Integer)         # bg_12
    client_name = Column(String(200))       # bg_13
    p_spec = Column(Integer)                # bg_16
    assignment_type = Column(String(20))    # bg_18
    business_area = Column(String(50))      # bg_21
    project_cc = Column(Integer)            # bg_26
    q1 = Column(Integer)                    # NKI1
    q2 = Column(Integer)                    # NKI2
    q3 = Column(Integer)                    # v_12
    q4 = Column(Integer)                    # Trade KPI
    q5 = Column(Integer)                    # v_15
    q6 = Column(Integer)                    # v_13
    q7 = Column(Integer)                    # NPS
    q8 = Column(String(3000))               # Improvements_text
    agr_prepared = Column(DateTime)         # bg_22
    agr_updated = Column(DateTime)          # bg_23
    survey_date = Column(DateTime)          # bg_52


