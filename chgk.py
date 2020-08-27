import pickle
import lxml.html
import lxml.etree
import requests
import urllib.parse
main_page = lxml.html.fromstring(requests.get('http://db.chgk.info/').text.strip())

n = main_page.\
            xpath('//li[contains(@class, \'pager-last\')]/a/@href')[0].\
            split('=')[-1]

tours = []

for n in range(int(n) + 1):
    nth_page = lxml.html.fromstring(requests.get('http://db.chgk.info/?page=' + str(n)).text.strip())
    tours.extend(nth_page.xpath('//tr/td[1]/a/@href'))

for tour in tours:
    tour_page = lxml.html.fromstring(requests.get(urllib.parse.urljoin('http://db.chgk.info/', tour)).text.strip())
    questions = tour_page.xpath('//div[contains(@class, \'question\')]')
    data = []
    for question in questions:
        q = (question.xpath('.//strong[contains(@class, \'Question\')]/following-sibling::text()'))
        a = (question.xpath('.//strong[contains(@class, \'Answer\')]/following-sibling::text()'))
        data.append((q, a))
    with open('chgk.pickle', 'ab') as f:
        pickle.dump(data, f)
