from models import CompanyName, Company,DBSession
# list_of_companies = open('Lists_of_companies/Компанії, що покинули ринок.txt','r',encoding='utf-8')
#
# for i in list_of_companies.readlines():
#     i = i.replace('-','').strip()
#     names = re.split('[:,]',i)
#     company = Company()
#     DBSession.add(company)
#     for name in names:
#         name = name.lstrip()
#         company_name = CompanyName(name=name,company=company)
#         DBSession.add(company_name)
# DBSession.commit()



def update_company_description(company_name: str, company_id: int, description: str):
    session = DBSession()
    company = session.query(Company).get(company_id)

    if company:
        # Check if the company name already exists
        existing_name = session.query(CompanyName).filter_by(name=company_name, company_id=company_id).first()

        if existing_name:
            existing_name.company.description = description
        else:
            # Add new CompanyName record
            company_name_record = CompanyName(name=company_name, company_id=company_id)
            session.add(company_name_record)
            company.description = description

        session.commit()
        print(f"Updated description for {company_name}")
    else:
        print(f"Company with ID {company_id} not found")





def update_description_by_id_range(start_id: int, end_id: int, new_description: str):
    session = DBSession
    session.query(Company).filter(Company.id >= start_id, Company.id <= end_id).update({Company.description: new_description})
    session.commit()




def delete_companies_range(start_id, end_id):
    session = DBSession
    try:
        session.query(Company).filter(Company.id >= start_id, Company.id <= end_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()