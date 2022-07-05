from selenium import webdriver
from config import user, host, password, db_name
import psycopg2
from selenium.webdriver.common.by import By

# Uncomment it for creation table
# Creation of database
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
#     with connection.cursor() as cursor:
#         cursor.execute(
#             """CREATE TABLE parser(
#                 id serial primary key,
#                 job_name varchar(1801),
#                 company_name varchar(1802),
#                 description varchar(29000));"""
#         )
#         connection.commit()
#         print("[Table created successfully]")
#     connection.close()
# except Exception as _ex:
#     print("[INFO] error while working with PostgreSQL", _ex)


# main function
def main():
    driver = webdriver.Chrome()
    driver.get(
        'https://hh.kz/search/vacancy?area=160&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post&hhtmFrom=vacancy_search_list')
    # Testcase for running program
    # main_element = driver.find_element(by=By.CLASS_NAME, value='vacancy-serp-item')
    # print(main_element)
    job_name = driver.find_elements(by=By.TAG_NAME, value="h3")
    company_name = driver.find_elements(by=By.CLASS_NAME, value="vacancy-serp-item__meta-info-company")
    description = driver.find_elements(by=By.CLASS_NAME, value="g-user-content")
    data1 = [120]
    data2 = [120]
    data3 = [120]
    # For loop for checking progress
    for c in description:
        data1.append(c.text)
    for j in company_name:
        data2.append(j.text)
    for i in job_name:
        data3.append(i.text)
    print(len(data1))
    print(len(data2))
    print(len(data3))
    data = [tuple(data1), tuple(data2), tuple(data3)]


# Inserting values into database
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO parser(description, company_name, job_name)
                VALUES(%s, %s, %s);""", (data[0], data[1], data[2], )
                )

        # with connection.cursor() as cursor:
        #     for d in data:
        #         cursor.execute(
        #             """INSERT INTO parser(description, company_name, job_name)
        #             VALUES(%s, %s, %s);""", d
        #             )

        connection.commit()
        print("[Data was successfully inserted into database]")
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
