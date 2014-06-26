import threading, requests, time, logging, httplib, uuid
from django.utils import timezone
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, SiteCheck, SiteCheckResult
from bs4 import BeautifulSoup
from sslscout.views import EngineLog, SaveRequest
#from sslscout.emails import ResultEmail

class www_ssllabs_com(threading.Thread):
    def __init__(self, sitecheckid):
        super(www_ssllabs_com, self).__init__()
        self.sitecheckid=sitecheckid


    def parse_results(self,result,parsed_html):
        try:
            ### find out if an error occurred
            warningdiv = parsed_html.find('div', attrs={'id': 'warningBox'})
            errordiv = parsed_html.find('div', attrs={'class': 'submitError'})
            if warningdiv:
                ### check failed, save the reason and abort
                result.error_string = warningdiv.text
            elif errordiv:
                ### check failed, save the reason and abort
                result.error_string = errordiv.text
            else:
                ### get the server IP
                result.serverip = parsed_html.find('div', attrs={'class': 'reportTitle'}).find('span',attrs={'class': 'ip'}).text.strip()[1:-1]

                ### get the results
                summarydiv = parsed_html.find_all('div', attrs={'class': 'sectionTitle'},text='Summary')[0].parent
                result.overall_rating = summarydiv.find('div',attrs={'class': 'ratingTitle'}).findNextSiblings('div')[0].text.strip()
                result.certificate_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Certificate').parent.find('div',attrs={'class': 'chartValue'}).text.strip())
                result.protocolsupport_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Protocol Support').parent.find('div',attrs={'class': 'chartValue'}).text.strip())
                result.keyexchange_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Key Exchange').parent.find('div',attrs={'class': 'chartValue'}).text.strip())
                result.cipherstrength_score = int(summarydiv.find('div',attrs={'class': 'chartLabel'},text='Cipher Strength').parent.find('div',attrs={'class': 'chartValue'}).text.strip())
                result.finish_time = timezone.now()
        except Exception as E:
            result.error_string = "exception in parse_results: %s" % E
        
        ### validate data
        try:
            result.full_clean()
        except Exception as E:
            ### unset usersupplied data except the IP
            result.error_string = "exception validating results: %s" % E.message_dict
            result.overall_rating = None
            result.certificate_score = None
            result.protocolsupport_score = None
            result.keyexchange_score = None
            result.cipherstrength_score = None

        
        ### return the result
        return result


    def run(self):
        ### initialize HTTP debug logging
        #logging.basicConfig()
        #logging.getLogger().setLevel(logging.DEBUG)
        #requests_log = logging.getLogger("requests.packages.urllib3")
        #requests_log.setLevel(logging.DEBUG)
        #requests_log.propagate = True

        ### get the sitecheck
        sitecheck = SiteCheck.objects.get(id=self.sitecheckid)
        
        ### log a message
        EngineLog(sitecheck,"checking site %s" % sitecheck.hostname)

        ### put the URLs together
        clearurl = sitecheck.engine.cacheclearurl + sitecheck.hostname
        url = sitecheck.engine.checkurl + sitecheck.hostname
        cachecleared = False
        
        ### begin requests session
        s = requests.Session()
        
        ### main loop to send requests to check for results periodically
        while True:
            try:
                ### generate a uuid for this request,
                ### and put the headers dict together
                requestuuid = str(uuid.uuid4())
                ua = 'sslscout engine request %s (python-requests/2.2.1 CPython/2.7.6 FreeBSD/9.2-STABLE)' % requestuuid
                headers = {
                    'User-Agent': ua,
                    'From': 'engine@sslscout.com'
                }

                ### make the request
                if cachecleared:
                    r = s.get(url,headers=headers)
                else:
                    r = s.get(clearurl,headers=headers)
                    cachecleared = True
                SaveRequest(request=r,sitecheck=sitecheck,uuid=requestuuid)
                r.raise_for_status()
                parsed_html = BeautifulSoup(r.text)
            except Exception as E:
                EngineLog(sitecheck,"exception getting and parsing html from %s: %s" % (url,E))
                sitecheck.finish_time = timezone.now()
                sitecheck.save()
                break

            ### find out if the check is finished or not by checking for the refresh tag
            refresh = parsed_html.find('meta', attrs={'http-equiv': 'refresh'})
            if refresh:
                #delay = int(refresh.get('content').split(";")[0])
                #print "sleeping %s seconds, got meta-refresh tag: %s" % (delay,refresh)
                time.sleep(40)
                continue
            else:
                ### no refresh tag found, this check is now finished, 
                ### extract the result data from the html, 
                ### but first find out if this is a single or multiple servers
                multipletable = parsed_html.find('table', attrs={'id': 'multiTable'})
                if not multipletable:
                    ### create the result object
                    result = SiteCheckResult(sitecheck=sitecheck)
                    self.parse_results(result,parsed_html)
                    result.save()
                else:
                    for server in multipletable.find_all('span',attrs={'class': 'ip'}):                        
                        ### get and parse the details page for this server
                        try:
                            requestuuid = str(uuid.uuid4())
                            ua = 'sslscout engine request %s (python-requests/2.2.1 CPython/2.7.6 FreeBSD/9.2-STABLE)' % requestuuid
                            headers = {
                                'User-Agent': ua,
                                'From': 'engine@sslscout.com'
                            }
                            r = s.get(sitecheck.engine.checkurl + server.find('a')['href'].split('?')[1][2:],headers=headers)
                            SaveRequest(request=r,sitecheck=sitecheck,uuid=requestuuid)
                            r.raise_for_status()
                            parsed_html = BeautifulSoup(r.text)
                        except Exception as E:
                            EngineLog(sitecheck,"exception getting and parsing html from %s: %s" % (url,E))
                            sitecheck.finish_time = timezone.now()
                            sitecheck.save()
                            break

                        ### parse and save the results
                        result = SiteCheckResult(sitecheck=sitecheck)
                        result.save()
                
                ### mark the sitecheck as finished
                sitecheck.finish_time = timezone.now()
                sitecheck.save()
                break

        ### log a message
        EngineLog(sitecheck,"finished checking site %s" % sitecheck.hostname)
        
        ### check if the result needs to be emailed to the user
        #if result_changed(sitecheck):
            # send email
            #formatdict = {
            #    'hostname': None
            #
            #}



class sslcheck_globalsign_com(threading.Thread):
    def __init__(self, sitecheckid):
        super(Worker, self).__init__()
        self.sitecheckid=sitecheckid
        
    def run(self):
        ### get the sitecheck
        sitecheck = SiteCheck.objects.get(id=sitecheckid)

