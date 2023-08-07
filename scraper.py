from selenium import webdriver
from selenium.webdriver.common.by import By


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def scrape_lifetime_gross():
    driver = webdriver.Chrome()
    driver.get(
        "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW")

    table_element = driver.find_element(By.TAG_NAME, "tbody")
    table_entry_elements = table_element.find_elements(By.TAG_NAME, "tr")

    data_table = []
    for entry in table_entry_elements:
        try:
            entry_data = entry.find_elements(By.TAG_NAME, "td")

            rank = len(data_table) + 1
            name = entry_data[1].find_element(By.TAG_NAME, "a").text
            year = int(entry_data[7].text)

            gross_filter = {',': '', '$': '', '-': '0'}
            percentage_filter = {',': '', '%': '', '<0.1': '0', '-': '0'}

            world_gross = int(replace_all(entry_data[2].text, gross_filter))
            domestic_gross = int(replace_all(entry_data[3].text, gross_filter))
            foreign_gross = int(replace_all(entry_data[5].text, gross_filter))
            domestic_percentage = float(replace_all(
                entry_data[4].text, percentage_filter))
            foreign_percentage = float(replace_all(
                entry_data[6].text, percentage_filter))

            """ JSON FORMAT
            movie_data = {"name": name, "year": year,
                          "worldLifetimeGross": world_gross,
                          "domesticLifetimeGross": domestic_gross,
                          "foreignLifetimeGross": foreign_gross,
                          "domesticPercentage": domestic_percentage,
                          "foreignPercentage": foreign_percentage} """

            # SQL FORMAT
            movie_data = (rank, name, year, world_gross,
                          domestic_gross, foreign_gross,
                          domestic_percentage, foreign_percentage)
            data_table.append(movie_data)
        except Exception as error:
            print('Caught this error: ' + repr(error))

    print(data_table)
    driver.close()

    return data_table
