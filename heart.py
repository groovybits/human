#!/usr/bin/python

"""
@project Heart
@author Chris Kennedy (c@groovy.org)

Heart.py - calculates different fib variations
"""

import time
import sys, getopt
from threading import Thread
from threading import BoundedSemaphore

class Beat:
    timebase = 12
    def beat(self, num):
        if num <= self.timebase:
                return num

        retnum = 0
        for i in range((self.timebase+2)):
            if i <= 0:
                continue
            retnum += self.beat(num - i)
        return retnum

    def space(self, t):
        time.sleep(t/self.timebase)

class Heart(Beat):
    active_threads = 0
    start_time = 0.0
    brain = []
    results = []
    def __init__(self, name, timebase = 12, processors = 1):
        print "Class Heart activated for \"", name, "\""
        self.start_time = time.time();
        self.timebase = timebase
        self.processors = processors
        self.active_sem = BoundedSemaphore(value=1)

    def set_beat(self, timebase):
        self.timebase = timebase

    def set_processors(self, processors):
        self.processors = processors

    def get_time(self):
        return (time.time() - self.start_time)

    def heart_beat(self, i):
        self.active_sem.acquire()
        self.active_threads += 1
        self.active_sem.release()
        begin = time.time()
        t = self.beat(i)
        msg = "%d) time %0.6f space %d" % (i, (time.time()-begin), t)
        self.results.append(msg)
        self.active_sem.acquire()
        self.active_threads -= 1
        self.active_sem.release()

    def print_results(self):
        # print results
        if (len(self.results)):
            for result in self.results:
                print result
            del self.results[:]

    def breath(self, num):
        for i in range(num):
            while self.active_threads >= self.processors:
                time.sleep(.10)
            # new thread
            t = Thread(target=self.heart_beat, args=(i,))
            # get lock
            t.setDaemon(True)
            t.start()
            self.brain.append(t)
            self.print_results()

        # Wait for all threads to exit
        while self.active_threads > 0:
            time.sleep(.10)

        self.print_results()

def main(argv):
   count = 16
   timebase = 12
   processors = 1
   try:
       opts, args = getopt.getopt(argv,"c:b:p:",
                                  ["count=", "base=", "processors="])
   except getopt.GetoptError:
       print 'test.py -c <count> -b <time base> -p <processors>'
       sys.exit(2)

   for opt, arg in opts:
       if opt in ("-c", "--count"):
           count = int(arg,10)
       elif opt in ("-b", "--base"):
           timebase = int(arg,10)
       elif opt in ("-p", "--processors"):
           processors = int(arg,10)

   heart = Heart("I", timebase, processors)
   heart.breath(count)
   t = heart.get_time()

   print "Life is at %f seconds" % t

if __name__ == "__main__":
    main(sys.argv[1:])
