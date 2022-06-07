import logging, os, sys
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../data/england/ofsted/')

def main():
  """
  Get latest Ofsted inspections CSV

  Scrapes GOV.UK webpage with links to Ofsted inspection outcomes data and
  streams CSV file with latest data to stdout.
  """

  log.info('Looking for link to latest Ofsted CSV data from GOV.UK')
  url = "https://www.gov.uk/government/statistical-data-sets/monthly-management-information-ofsteds-school-inspections-outcomes"

  response = requests.get(url)
  if not response.ok:
    log.error(f'Could not get Ofsted inspection outcomes page, received {response.status_code} response')
    sys.exit()

  soup = BeautifulSoup(response.text, 'html.parser')

  try:
    csv_link = soup.select('.attachment .download a')[0]
    href = csv_link['href']
  except (IndexError, IndexError):
    log.error('Failed to find CSV download link in Ofsted inspection outcomes page')
    sys.exit()

  path = urlparse(href).path
  filename = os.path.basename(path)

  if not filename.endswith('.csv'):
    log.error(f'Filename {filename} does not have an extension of .csv')
    sys.exit()

  response = requests.get(href, stream = True)
  if not response.ok:
    log.error(f'Could not download latest Ofsted CSV file, received {response.status_code} response')
    sys.exit()

  for line in response.iter_lines(decode_unicode=True):
    if line:
      print(line)

if __name__ == '__main__':
  main()