from datetime import datetime

import requests
from bs4 import BeautifulSoup

def scraper(url):
    #url = "https://www.shabdkosh.com/word-of-the-day/english-hindi/"
    html = requests.get(url)

    s = BeautifulSoup(html.content, 'html.parser')
    WordOftheDaySection = s.find(class_='border px-2 mb-3 rounded bg-light text-center my-2')
    DateSection = s.find(class_='col-lg-8 col-md-7')
    #Extract words
    word_of_the_day_in_english = WordOftheDaySection.find('p', class_='pt-3').find('a').text
    word_of_the_day_in_hindi = WordOftheDaySection.find('p', class_='pt-3').find_all('a')[1].text

    #Extract usage example
    english_usage_example = WordOftheDaySection.find_all('p')[1].text
    hindi_usage_example = WordOftheDaySection.find_all('p')[2].text

    date_element = DateSection.find('p').find('time').text
    date_obj = datetime.strptime(date_element, "%B %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    print("Date", formatted_date)
    print("Word of the Day in English:", word_of_the_day_in_english)
    print("Word of the Day in Hindi:", word_of_the_day_in_hindi)
    print("English Usage Example:", english_usage_example)
    print("Hindi Usage Example:", hindi_usage_example)

    scraped_data = {
        'date': formatted_date,
        'wordOfTheDayinEnglish': word_of_the_day_in_english,
        'wordOfTheDayinHindi': word_of_the_day_in_hindi,
        'wordOfTheDayinEnglish_Usage_Example': english_usage_example,
        'wordOfTheDayinHindi_Usage_Example': hindi_usage_example,
    }

    return scraped_data




'''
def scraper(url):
    try:
        # Set the path to your Edge WebDriver executable for Linux
        webdriver_path = '/home/kidastudios/Desktop'

        # Create an Edge WebDriver service
        service = EdgeService(webdriver_path)

        # Start a new Edge browser session
        driver = webdriver.Edge(service=service)

        # Navigate to the webpage
        driver.get(url)

        # Locate the <div> element containing the word of the day
        word_of_the_day_div = driver.find_element(By.CLASS_NAME, 'border')

        # Extract the word in English
        word_of_the_day_in_english = word_of_the_day_div.find_element(By.XPATH, './a[1]').text

        # Extract the word in Hindi
        word_of_the_day_in_hindi = word_of_the_day_div.find_element(By.XPATH, './a[2]').text

        # # Extract the English usage example this is wrong
        # english_usage_example = driver.find_element(By.XPATH, '//p[contains(., "The difference between information and knowledge may seem very subtle")]').text
        #
        # # Extract the Hindi usage example this is wrong
        # hindi_usage_example = driver.find_element(By.XPATH, '//p[contains(., "सूचना और ज्ञान के बीच बहुत हल्का अंतर होता है, लेकिन युद्ध में यही अंतर बहुत महत्वपूर्ण हो जाता है।")]').text

        # Locate the <time> element containing the date
        date_element = driver.find_element(By.CLASS_NAME, 'updated')

        # Extract the date
        date = date_element.text
        date_obj = datetime.strptime(date, "%B %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        # Create a dictionary to store the scraped data
        scraped_data = {
            'date': formatted_date,
            'word_of_the_day_in_english': word_of_the_day_in_english,
            'word_of_the_day_in_hindi': word_of_the_day_in_hindi,
            #'english_usage_example': english_usage_example,
            #'hindi_usage_example': hindi_usage_example,
        }

        return scraped_data

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None

    finally:
        # Close the browser session
        driver.quit()
        '''
