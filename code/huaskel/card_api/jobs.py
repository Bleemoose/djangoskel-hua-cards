# Schedule Tasks
from schedule import Scheduler
import threading
import time
from .models import *
from accounts.models import User
import os
import logging

logger = logging.getLogger('card_api')


def pingStations():
    logger.info('Checking station status')
    stations = Station.objects.all()

    for i in range(stations.__len__()):
        hostname = stations[i].station_address
        response = os.system('ping -c 1 ' + hostname)

        # and then check the response...
        if response == 0:
            print(stations[i].__str__() + ' is up!')
        else:
            print(stations[i].__str__() + ' is down!')
            logger.warning('Station: %s is down!', stations[i].__str__())


def fixPendingRegistries():
    logger.info('Checking if there are any pending checkouts')
    users = User.objects.all()
    for i in range(users.__len__()):
        registries = CardRegistries.objects.filter(owner_id=users[i].id)

        if not(registries[registries.__len__()-1].is_checkout):
            #!IMPORTANT!#
            #For this card registry to work it means that at least 1 station exists and the user still has one card assigned, this can lead to bugs further down
            #TODO fix this?
            registry_obj = CardRegistries(owner=users[i], station_id=Station.objects.all()[0].id, card_id=Card.objects.get(owner=users[i]).id,is_checkout=True)
            registry_obj.save()
            logger.info('Automatically checked out user : %s',users[i])


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every(10).minutes.do(pingStations)
    scheduler.every().day.at('23:50').do(fixPendingRegistries)
    scheduler.run_continuously()
