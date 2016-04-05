import pickle
import collections
import fcntl
import subprocess

from time import sleep

if __name__ == '__main__':

    setup_output = subprocess.check_output(['fast-gpio', 'set-input', '7'])
    print setup_output

    d = collections.deque(maxlen=100)
    while True:
        read_output = subprocess.check_output(['fast-gpio', 'read', '7'])
        d.append(read_output[-2])
        print read_output[-2]
        # f = open("save.p","wb")
        # try:
        #    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        #    pickle.dump(d, f)
        # except IOError as e:
        #    print 'err in startAccel'
        #        #raise on unrelated IOErrors
#           if e.errno != errno.EAGAIN:
#                    print 'err in startAccel'
#                    print str(e.errno)
        #f.close()
        sleep(1)


def roomOccupied(samples):
    sumSamples = 0
    for sample in samples:
        if int(sample) == 1:
            sumSamples += 1
        print sample
    print "total 1s: " + str(sumSamples)
    print "total length: " + str(len(samples))
    return sumSamples > (len(samples)/4)

