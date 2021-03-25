#
# Logging routines for trax
#

from datetime import datetime
import sys

class Logger:
    # Class variables
    filehandle = 0
    filename = 0
    default_filename = '/var/log/trax.log'

    def __init__(self, logfile=0):
        if (sys.stdin.isatty() and not logfile):
            Logger.filehandle = sys.stdout
            Logger.filename = 'STDOUT'
            self.info("TTY detected; logging to stdout")
        else:
            Logger.filename = logfile if logfile else Logger.default_filename
            Logger.filehandle = sys.stdout
            #Logger.filehandle = open file for append

    def _dolog(self, level, msg):
        datestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Logger.filehandle.write("{} [{}] {}\n".format(datestr, level, msg))

    def info(self, *msg, sep=' '):
        self._dolog('INFO', sep.join(msg))

    def warn(self, *msg, sep=' '):
        self._dolog('WARN', sep.join(msg))

    def error(self, *msg, sep=' '):
        self._dolog('ERR', sep.join(msg))



# Unit testing
if __name__ == "__main__":
    l = Logger()
    l.info('This is', 'an', "INFO message")
    l.warn("This is a WARn message")
    l.error('This is a ERROR message')
    l.info('This is', str(1), 'message')
