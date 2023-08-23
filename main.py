import os
import requests
import selectorlib
import smtplib
import ssl
import time
import sqlite3 as sql

# create a connection
connection = sql.connect("data.db")

URL = "http://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    # scrapes data from webpage
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    # uses yaml file to get source from the webpage
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "testingpythonapp@gmail.com"
    password = os.getenv('PASSWORD')

    receiver = "testingpythonapp@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email was sent")


def store(extracted1):
    # split the content using commas
    row = extracted1.split(',')
    # get rid of unnecessary spaces
    row = [item.strip() for item in row]
    # cursor serves as an object that executes SQL methods
    cursor = connection.cursor()
    # insert values into new rows
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    #  write changes into database
    connection.commit()


def read(extracted2):
    # split the content using commas
    row = extracted2.split(',')
    # get rid of unnecessary spaces
    row = [item.strip() for item in row]
    band, city, date = row
    # cursor serves as an object that executes SQL methods
    cursor = connection.cursor()
    # query data inside cursor object
    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?",
                   (band, city, date))
    # used to catch all instances of the select criteria
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    # While loop is made to keep program running
    while True:
        # calls the scrape function
        scraped = scrape(URL)
        # calls the extract function
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            # call read function with the extracted variable
            content = read(extracted)
            # check to see if content is empty
            if not content:
                store(extracted)
                # sends email to user
                send_email(message=f"New event {extracted} was found")

        time.sleep(3)
