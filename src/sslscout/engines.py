import threading, requests, time, logging, httplib
from django.utils import timezone
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, SiteCheck, SiteCheckResult
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

        ### put the URLs together
        clearurl = sitecheck.engine.cacheclearurl + sitecheck.hostname
        url = sitecheck.engine.checkurl + sitecheck.hostname
        cachecleared = False
        
        ### begin requests session
        s = requests.Session()
        
        ### make the check for results every 5 seconds
        while True:
            try:
                ### make the request
                if cachecleared:
                    r = s.get(url)
                else:
                    r = s.get(clearurl)
                    cachecleared = True
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
                ### no refresh tag found, this check is now finished, 
                ### extract the result data from the html, first find out if this is a single or multiple servers
                multipletable = parsed_html.find('table', attrs={'id': 'multiTable'})
                if not multipletable:
                    ### create the result object
                    result = SiteCheckResult(sitecheck=sitecheck)
                    
                    ### get the server IP
                    result.ip = parsed_html.find('div', attrs={'class': 'reportTitle'}).find('span',attrs={'class': 'ip'}).text
                    
                    ### get the results
                    summarydiv = parsed_html.find_all('div', attrs={'class': 'sectionTitle'},text='Summary')[0].parent
                    result.overall_rating = summarydiv.find('div',attrs={'class': 'rating_g'}).text
                    result.certificate_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Certificate').parent.find('div',attrs={'class': 'chartValue'}).text)
                    result.protocolsupport_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Protocol Support').parent.find('div',attrs={'class': 'chartValue'}).text)
                    result.keyexchange_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Key Exchange').parent.find('div',attrs={'class': 'chartValue'}).text)
                    result.cipherstrength_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Cipher Strength').parent.find('div',attrs={'class': 'chartValue'}).text)
                    result.finish_time = timezone.now()
                    result.save()
                else:
                    for server in multipletable.find_all('span',attrs={'class': 'ip'}):
                        result = SiteCheckResult(sitecheck=sitecheck)
                        
                        ### get and parse the details page for this server
                        try:
                            r = s.get(sitecheck.engine.checkurl + server.find('a')['href'].split('?')[1][2:])
                            r.raise_for_status()
                            parsed_html = BeautifulSoup(r.text)
                        except Exception as E:
                            print "exception getting and parsing html from %s: %s" % (url,E)
                            sitecheck.finish_time = timezone.now()
                            sitecheck.save()
                            break

                        result.ip = parsed_html.find('div', attrs={'class': 'reportTitle'}).find('span',attrs={'class': 'ip'}).text
                        summarydiv = parsed_html.find_all('div', attrs={'class': 'sectionTitle'},text='Summary')[0].parent
                        result.overall_rating = summarydiv.find('div',attrs={'class': 'rating_g'}).text
                        result.certificate_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Certificate').parent.find('div',attrs={'class': 'chartValue'}).text)
                        result.protocolsupport_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Protocol Support').parent.find('div',attrs={'class': 'chartValue'}).text)
                        result.keyexchange_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Key Exchange').parent.find('div',attrs={'class': 'chartValue'}).text)
                        result.cipherstrength_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Cipher Strength').parent.find('div',attrs={'class': 'chartValue'}).text)
                        result.finish_time = timezone.now()
                        result.save()
                break

        ### thread finished

        
class sslcheck_globalsign_com(threading.Thread):
    def __init__(self, sitecheckid):
        super(Worker, self).__init__()
        self.sitecheckid=sitecheckid
        
    def run(self):
        ### get the sitecheck
        sitecheck = SiteCheck.objects.get(id=sitecheckid)

