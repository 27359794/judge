import subprocess, threading
#import os
import time

EXE_NAME = 'compiled'

EXIT_SUCCESS = 0
TIMEOUT = -15
SEGFAULT = 139


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def runTest(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True, stderr=subprocess.PIPE)
            self.process.communicate()

        thread = threading.Thread(target=target)

        thread.start()
        startTime = time.time()
        thread.join(timeout)

        if thread.is_alive():
            killRunning()

        endTime = time.time()

        if endTime - startTime > timeout:
            return TIMEOUT, timeout
        else:
            assert self.process.returncode != None
            return self.process.returncode, endTime-startTime


    def runCommand(self):
        return subprocess.Popen(self.cmd, shell=True, stderr=subprocess.PIPE).stderr.read()


def test(timeLimit, caseNum, fin, fout, casesPath):
    prepareInput(casesPath, caseNum, fin)
    returnCode, timeTaken = Command('./compiled').runTest(timeLimit)

    reason = 'crashed'

    if returnCode == EXIT_SUCCESS:
        reason = 'correct' if correctOutput(casesPath, caseNum, fout) else 'incorrect'
    elif returnCode == TIMEOUT:
        reason = 'timeout'
    elif returnCode == SEGFAULT:
        reason = 'crashed (segfault)'

    cleanup(fin, fout)
    return reason, timeTaken


def correctOutput(casesPath, caseNum, fout):
    return simplify(open(casesPath + ('/out/%d.out'%caseNum)).read()) == \
           simplify(open(fout).read())


def cleanup(fin, fout):
    Command('rm %s %s' % (fin, fout)).runCommand()

def killRunning():
    Command('killall compiled').runCommand()

def simplify(text):
    lines = []
    for line in text.strip().split('\n'):
        lines.append(line.strip().split())
    return lines


def prepareInput(casesPath, caseNum, fin):
    cmdStr = 'cp %s/in/%d.in ./%s' % (casesPath, caseNum, fin)
    Command(cmdStr).runCommand()
