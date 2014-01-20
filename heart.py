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
from multiprocessing import Process, Queue

class Beat:
    timebase = 12
    def beat(self, num, q = 0):
        try:
            if num <= self.timebase:
                if q:
                    q.put(num)
                return num

            retnum = 0
            for i in range((self.timebase+2)):
                if i <= 0:
                    continue
                ret = self.beat(num - i)
                retnum = retnum + ret
            if q:
                q.put(retnum)
        except KeyboardInterrupt:
            sys.exit(1)
        return retnum

    def iam(self, num):
        try:
            q = Queue()
            p = Process(target=self.beat, args=(num,q))
            p.start()
            p.join()
        except KeyboardInterrupt:
            sys.exit(1)
        return q.get()

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
        t = self.iam(i)
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
                self.print_results()
                time.sleep(.25)
            # new thread
            #print "Starting thread ", self.active_threads+1, " for ", i
            t = Thread(target=self.heart_beat, args=(i,))
            # get lock
            t.setDaemon(True)
            t.start()
            self.brain.append(t)
            self.print_results()

        # Wait for all threads to exit
        while self.active_threads > 0:
            self.print_results()
            time.sleep(.25)

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

   try:
        heart = Heart("I", timebase, processors)
        heart.breath(count)
        t = heart.get_time()
   except KeyboardInterrupt:
        print "Exiting, killing processes"
        sys.exit(1)

   print "Life is at %f seconds" % t

if __name__ == "__main__":
    main(sys.argv[1:])
