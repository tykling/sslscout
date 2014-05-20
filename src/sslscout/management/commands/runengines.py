from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import timedelta
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, SiteCheck, SiteCheck
from sslscout.engines import www_ssllabs_com, sslcheck_globalsign_com
from threading import Thread
import os, socket, sys, datetime

class Command(BaseCommand):
    args = 'none'
    help = 'Find idle engines and sites that need checking and run checks'

    
    ### function to run sitechecks
    def handle(self, *args, **options):
        ### open listening socket (instead of writing a pidfile)
        pidsocket = "/tmp/sslscout-engine-%s.sock" % settings.ENVIRONMENT
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
        engines = CheckEngine.objects.filter(active=True)
        enginethreads = []
        for engine in engines:
            print "################################################################################"
            print "############ Working on engine %s ##############################################" % engine.name
            print "################################################################################"
            ### check if this engine already has a job running
            if SiteCheck.objects.filter(finish_time=None,engine=engine).exclude(start_time=None).count() > 0:
                ### skipping this engine
                self.stdout.write('engine %s is already busy running a job' % engine.name)
                continue
            
            ### find a site that needs checking
            sites = Site.objects.all()
            for site in sites:
                print "############ Working on site %s ##############################################" % site.hostname

                try:
                    ### find the latest sitecheck for this hostname with this engine
                    latest_sitecheck = SiteCheck.objects.filter(engine=engine,hostname=site.hostname).latest('finish_time')
                except SiteCheck.DoesNotExist:
                    ### no previous checks registered for this hostname
                    latest_sitecheck = None
                
                ### if we have a latest_sitecheck, find out if it is more than interval_hours old
                if latest_sitecheck:
                    if latest_sitecheck.finish_time + timedelta(hours=site.sitegroup.interval_hours) > timezone.now():
                        ### not yet
                        print "- this site does not need to be checked yet, skipping..."
                        continue

                ### OK, time to do a new check for this site
                print "- starting new sitecheck thread for this site..."

                sitecheck = SiteCheck(hostname=site.hostname,engine=engine)
                sitecheck.save()
                
                if engine.engineclass == 'www_ssllabs_com':
                    thread = www_ssllabs_com(sitecheck.id)
                elif engine.engineclass == 'sslcheck_globalsign_com':
                    thread = sslcheck_globalsign_com(sitecheck.id)
                else:
                    self.stdout.write('unknown engine, error')
                
                thread.start()
                enginethreads.append(thread)
                break

        ### finished looping through engines, wait for any spawned threads to finish
        if len(enginethreads) > 0:
            self.stdout.write('waiting for %s threads to finish...' % len(enginethreads))
            for et in enginethreads:
                et.join()

            ### all threads finished
            self.stdout.write('all threads finished')
            #for et in enginethreads:
            #    print et.result
        else:
            print "no threads started"

        print "done"
