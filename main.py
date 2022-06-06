from selenium import webdriver
from config import user, host, password, db_name
import psycopg2
from selenium.webdriver.common.by import By

# Creation of datbase
# try:
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
#     with connection.cursor() as cursor:
#         cursor.execute(
#             "SELECT version();"
#         )
#         print(f"Server version: {cursor.fetchone()}")
#
#     # with connection.cursor() as cursor:
#     #     cursor.execute(
#     #         """CREATE TABLE parser(
#     #             id serial primary key,
#     #             job_name varchar(80),
#     #             company_name varchar(80),
#     #             location varchar(80),
#     #             description varchar(360));"""
#     #     )
#     #     connection.commit()
#     #     print("[Table created successfully]")
#     connection.close()
# except Exception as _ex:
#     print("[INFO] error while working with PostgreSQL", _ex)


class ProgParser(object):

    def __init__(self):
        pass

    def parse(self):
        pass


def main():
    driver = webdriver.Chrome()
    driver.get(
        'https://hh.kz/search/vacancy?area=160&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post&hhtmFrom=vacancy_search_list')
    # main_element = driver.find_element(by=By.CLASS_NAME, value='vacancy-serp-item')
    # print(main_element)
    job_name = driver.find_elements(by=By.TAG_NAME, value="h3")
    company_name = driver.find_elements(by=By.CLASS_NAME, value="vacancy-serp-item__meta-info-company")
    description = driver.find_elements(by=By.CLASS_NAME, value="bloko-text_no-top-indent")
    ma_dict = {}
    for c in description:
        print("Description - ", c.text)
        ma_dict["Desc"] = c.text
    for j in company_name:
        print("Company name - ", j.text)
    for i in job_name:
        print(i.text)

# Inserting values
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            for j in job_name:
                cursor.execute(
                    """INSERT INTO parser(job_name)
                    VALUES(%s);""", (j.text,)
                    )
        with connection.cursor() as cursor:
            for j in company_name:
                cursor.execute(
                    """INSERT INTO parser(company_name)
                    VALUES(%s);""", (j.text,)
                )
        with connection.cursor() as cursor:
            for j in description:
                cursor.execute(
                    """INSERT INTO parser(description)
                    VALUES(%s);""", (j.text,)
                )

        connection.commit()
        print("[Table created successfully]")
        connection.close()
    except Exception as _ex:
        print("[INFO] error while working with PostgreSQL", _ex)

# Drop table
#     try:
#         connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name
#         )
#
#         with connection.cursor() as cursor:
#             cursor.execute("""DROP table parser""")
#
#         connection.commit()
#         print("[Table deleted successfully]")
#         connection.close()
#     except Exception as _ex:
#         print("[INFO] error while working with PostgreSQL", _ex)

if __name__ == '__main__':
    main()
