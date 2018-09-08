from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class ConsultingServicesTouchpoint(Base):
    __tablename__ = 'ConsultingServicesTouchPoint'
    idx = Column(Integer, primary_key=True)
    lfdn = Column(Integer, unique=True)         # lfdn
    project_number = Column(Integer)            # bg_08
    subproject_number = Column(String(15))        # bg_54
    client_name = Column(String(200))           # bg_09
    p_spec = Column(Integer)                    # bg_16
    assignment_type = Column(String(20))        # bg_18
    business_area = Column(String(50))          # bg_21
    project_cc = Column(Integer)                # bg_26
    q1 = Column(Integer)                        # NKI1
    q2 = Column(Integer)                        # NKI2
    q3 = Column(Integer)                        # v_12
    q4 = Column(Integer)                        # Trade_KPI
    q5 = Column(Integer)                        # NPS
    q6 = Column(String(3000))                   # Improvements_text
    agr_prepared = Column(DateTime)             # bg_22
    agr_updated = Column(DateTime)              # bg_23
    survey_date = Column(DateTime)              # bg_52