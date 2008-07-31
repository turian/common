
import random, time
def random(min, max):
    """ Sleep some random time in [min, max) """
    sleep = random.random() * (max - min) + min
    #sleep = random.random() * 2 + 0
    print "Sleeping %g seconds..." % sleep
    time.sleep(sleep)
