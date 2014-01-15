#!/usr/bin/python

import time
import sys, getopt

class Beat:
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
    timebase = 12
    start_time = 0.0;
    def __init__(self, name):
        print "Class Heart activated for \"", name, "\""
        self.start_time = time.time();

    def set_beat(self, timebase):
        self.timebase = timebase

    def get_time(self):
        return (time.time() - self.start_time)

    def breath(self, num):
        for i in range(num):
            begin = time.time()
            t = self.beat(i)
            #self.space(t)
            print "%d) time %0.6f space %d" % (i, (time.time()-begin), t)


def main(argv):
   count = 16
   try:
       opts, args = getopt.getopt(argv,"c:",["count="])
   except getopt.GetoptError:
       print 'test.py -c <count in base 12>'
       sys.exit(2)

   for opt, arg in opts:
       if opt in ("-c", "--count"):
           count = int(arg,12)

   heart = Heart("I")
   heart.breath(count)
   t = heart.get_time()

   print "Life is at %f seconds" % t

if __name__ == "__main__":
    main(sys.argv[1:])
