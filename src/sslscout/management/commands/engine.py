from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, SiteCheck, CheckResult
from sslscout.engines import www_ssllabs_com, sslcheck_globalsign_com
from threading import Thread
import os, socket, sys, datetime

class Command(BaseCommand):
    args = 'none'
    help = 'Find idle engines and sites that need checking and run checks'

    
    ### function to run sitechecks
    def runjob(self, *args, **options):
        ### open listening socket (instead of writing a pidfile)
        pidsocket = "/tmp/runjob.sock"
        if os.path.exists(pidsocket):
            ### bail out
            self.stdout.write('socket %s already exists, bailing out' % pidsocket)
            sys.exit(1)
        else:
            try:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                s.bind(pidsocket)
                os.unlink(pidsocket)
            except:
                self.stdout.write('unable to bind pidsocket %s, bailing out' % pidsocket)
                sys.exit(1)

        ### get a list of active engines
        engines = CheckEngine.objects.get(active=True)
        enginethreads = []
        for engine in engines:
            ### check if this engine already has a job running
            if SiteCheck.objects.count(finish_time=None,engine=engine).count() > 0:
                ### skipping this engine
                self.stdout.write('engine %s is already busy running a job' % engine.name)
                continue
            
            ### find a site that needs checking
            sites = Site.objects.all()
            for site in sites:
                try:
                    latest_sitecheck = SiteCheck.objects.get(engine=engine,site=site).latest('finish_time')
                except DoesNotExist:
                    ### no previous checks registered for this site
                    latest_sitecheck = None
                
                ### if we have a latest_sitecheck, find out if it is more than interval_hours old
                if latest_sitecheck:
                    if latest_sitecheck.finish_time + timedelta(hours=site.sitegroup.interval_hours) > timezone.now():
                        ### not yet
                        continue

                ### OK, time to do a new check for this site
                sitecheck = SiteCheck(site=site,engine=engine)
                sitecheck.save()
                
                if engine.engineclass == 'www_ssllabs_com':
                    thread = www_ssllabs_com(sitecheck=sitecheck)
                elif engine.engineclass == 'sslcheck_globalsign_com':
                    thread = sslcheck_globalsign_com(sitecheck=sitecheck)
                else:
                    self.stdout.write('unknown engine, error')
                
                thread.start()
                enginethreads.append(thread)


        ### finished looping through engines, wait for any spawned threads to finish
        if len(enginethreads) > 0:
            self.stdout.write('waiting for %s threads to finish...' % len(enginethreads))
            for et in enginethreads:
                et.join()

            ### all threads finished
            self.stdout.write('all threads finished, results:')
            for et in enginethreads:
                print et.result
        else:
            print "no threads started"

        print "done"
