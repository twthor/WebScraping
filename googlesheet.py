from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# tthorportfo8453
SERVICE_ACCOUNT_FILE = 'C:/Users/tthor/Documents/Python/stockWebScraping/tthorportfo8453-f82c1ca82692.json' # key file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # .readonly på slutte om man ønsker det
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID spreadsheet.
SAMPLE_SPREADSHEET_ID = '1ucHdqccEGU0O7BTolDmIhNSIRiG93RMVlDUsFJMCIcY'
list_urls = ["https://www.nordnet.no/market/stocks/16105595-telenor", "https://www.nordnet.no/market/stocks/16121893-coca-cola-co",
"https://www.nordnet.no/market/stocks/16255141-amc-entertainment-holdings"]
# "https://www.norges-bank.no/tema/Statistikk/Valutakurser/?tab=currency&id=USD"

def web_scraping(url):
    page = requests.get(url)
    # print(page)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("span", class_="Typography__Span-sc-10mju41-0 gaHPGY Typography__StyledTypography-sc-10mju41-1 epuleM StatsBox__StyledPriceText-sc-163f223-2 djnBAa")
    # if url == "https://www.norges-bank.no/tema/Statistikk/Valutakurser/?tab=currency&id=USD":
    #     results = soup.find("span", class_="currency-transformer__number")
    #     results = list(results)
    #     results = results[:-4]
    #     results = str(results)
    #     print(results)
    # hb_results = soup.find("div", class_="ng-binding ng-scope")
    # results = soup.find("div", class_="Box_StyledDiv-sc-1bfv3i9-0 gBnipNb")
    # if results == str:
    #     return float(results.replace(",", "."))
    # else:
    return float(results.text.replace(",", ".")) # må endre komma til punktum for å konvertere string til float
#print(web_scraping())

def main():
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="portfolio!A24:C30").execute()
    values = result.get('values', []) # leser av verdiene.
    # print(values)

    # Lage en liste med verider jeg ønsker å skrive inn.
    pris_telenor = [[web_scraping(list_urls[0])]] # må være list of lists, selv med 1 verdi
    # Skal man skrive inn samme verdi i flere celler, må det ligge flere elementer av samme verdi i listen
    pris_CO = [[web_scraping(list_urls[1])]]
    pris_AMC = [[web_scraping(list_urls[2])]]
    # dollar_kurs = [[web_scraping(list_urls[3])]]
    
    list_stocks = [[pris_telenor, "L19"], [pris_CO, "K15"], [pris_AMC, "K20"]] # dollar_kurs, "F22"
    for i in range(len(list_stocks)):
        price_update = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=f"portfolio!{list_stocks[i][1]}", valueInputOption="USER_ENTERED", body={"values":list_stocks[i][0]}).execute()
    print(price_update)
    
if __name__ == '__main__':
    main()