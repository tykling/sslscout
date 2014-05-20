import threading, requests, time, logging, httplib
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, SiteCheck
from bs4 import BeautifulSoup

class www_ssllabs_com(threading.Thread):
    def __init__(self, sitecheckid):
        super(www_ssllabs_com, self).__init__()
        self.sitecheckid=sitecheckid

    def run(self):
        ### initialize HTTP debug logging
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

        ### get the sitecheck
        sitecheck = SiteCheck.objects.get(id=self.sitecheckid)

        ### put the URL together
        url = sitecheck.engine.checkurl + sitecheck.hostname
        
        ### begin requests session
        s = requests.Session()

        ### make the initial request
        r = s.get(url)
        
        ### check for result every 5 seconds
        while True:
            try:
                ### check if this check is finished
                r = s.get(url)
                r.raise_for_status()
                parsed_html = BeautifulSoup(r.text)
            except Exception as E:
                print "exception getting and parsing html from %s: %s" % (url,E)
                sitecheck.finish_time = timezone.now()
                sitecheck.save()
                break
                
            refresh = parsed_html.find_all('meta', attrs={'http-equiv': 'refresh'})
            if refresh:
                delay = int(parsed_html.find_all('meta', attrs={'http-equiv': 'refresh'})[0].get('content').split(";")[0])
                time.sleep(delay)
                continue
            else:
                ### no refresh tag found, this check is finished, extract the result data from the html
                sitecheck.debug_html = r.text
                summarydiv = parsed_html.find_all('div', attrs={'class': 'sectionTitle'},text='Summary')[0].parent
                sitecheck.overall_rating = summarydiv.find('div',attrs={'class': 'ratingTitle'},text='Overall Rating').parent.find('span').text
                sitecheck.certificate_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Certificate').parent.find('div',attrs={'class': 'chartValue'}).text)
                sitecheck.protocolsupport_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Protocol Support').parent.find('div',attrs={'class': 'chartValue'}).text)
                sitecheck.keyexchange_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Key Exchange').parent.find('div',attrs={'class': 'chartValue'}).text)
                sitecheck.cipherstrength_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Cipher Strength').parent.find('div',attrs={'class': 'chartValue'}).text)
                sitecheck.finish_time = timezone.now()
                sitecheck.save()
                break
        
        ### thread run finished

        
class sslcheck_globalsign_com(threading.Thread):
    def __init__(self, sitecheckid):
        super(Worker, self).__init__()
        self.sitecheckid=sitecheckid
        
    def run(self):
        ### get the sitecheck
        sitecheck = SiteCheck.objects.get(id=sitecheckid)

