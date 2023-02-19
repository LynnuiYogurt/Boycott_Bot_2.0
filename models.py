from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///db_companies.db", echo=True)
session_creator = sessionmaker(bind=engine)
DBSession = session_creator()
Base = declarative_base()



class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer(),primary_key=True)
    names = relationship('CompanyName',back_populates='company')
    description = Column(String(),nullable=True)

class CompanyName(Base):
    __tablename__ = "company_names"

    id = Column(Integer(), primary_key=True)
    name = Column(String(),nullable=False)
    company_id = Column(ForeignKey('companies.id'),nullable=False)
    company = relationship('Company',back_populates='names')


if __name__ == '__main__':
    Base.metadata.create_all(engine)




