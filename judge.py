"""
judge.py
Daniel Goldbach, 2010

Judge a C/++ program, contest-style.

"""

import os
import test
import argparse

def compileAndJudge(sourceFileName, fin, fout, pathToCases, timeLimit):
    header(sourceFileName, fin, fout, 'weights.txt' in os.listdir(pathToCases))

    escaped = escape(sourceFileName)
    compilerOut = None

    if sourceFileName.endswith('.c'):
        compilerOut = test.Command('gcc -o compiled -m32 -Wall -O2 -lm ' + escaped).runCommand()
    elif sourceFileName.endswith('.cpp') or sourceFileName.endswith('.cc'):
        compilerOut = test.Command('g++ -o compiled -m32 -Wall -O2 -lm ' + escaped).runCommand()
    elif sourceFileName.endswith('.py'):
        # TODO: this
        assert False
    else:
        raise OSError('file format of \'%s\' not recognised' % sourceFileName)

    if 'compiled' not in os.listdir('.'):
        box2Text('COMPILATION FAILED:\n' + compilerOut)
    else:
        numCases = len(filter(lambda s: s.endswith('.in'), os.listdir(pathToCases + '/in')))
        judge(numCases, fin, fout, timeLimit, pathToCases)

        test.Command('rm compiled').runCommand()


def judge(numCases, fin, fout, timeLimit, casesPath):
    print 'JUDGE'
    print 'CASES: Num | Score |       Reason      |   Time'
    print '       ----+-------+-------------------+----------'
    scores = []

    for i in xrange(1, numCases+1):
        reason, timeTaken = test.test(timeLimit, i, fin, fout, casesPath)

        # retest for niceness
        if (reason == 'timeout'):
            reason, timeTaken = test.test(timeLimit, i, fin, fout, casesPath)

        score = 100 if reason == 'correct' else 0
        scores.append(score)
        print format(i, score, reason, timeTaken)

    print 'Score for this submission: %d%%\n' % getFinalScore(scores, casesPath)


def header(sourceFileName, fin, fout, weightsFound):
    boxText('''
SOURCE FILE: %s
INPUT:       %s
OUTPUT:      %s
WEIGHTED:    %s
''' % (sourceFileName.split('/')[-1], fin, fout, bool(weightsFound)))

def format(caseNum, score, reason, timeTaken):
    caseNumStr = ('#'+str(caseNum)).rjust(10) + ' '
    scoreStr = str(score).center(7)
    reasonStr = ' ' + str(reason).ljust(18)

    if reason == 'timeout':
        timeStr = ''
    else:
        timeStr = ('%.3f'%timeTaken).rjust(8) + 's'

    return '%s|%s|%s|%s' % (caseNumStr, scoreStr, reasonStr, timeStr)


def boxText(text):
    print '\n+-------------------------------------------------------+'
    for line in text.strip().split('\n'):
        print '| ' + line
    print '+-------------------------------------------------------+\n'


def box2Text(text):
    print '\n****************************************'
    for line in text.strip().split('\n'):
        print '* ' + line
    print '****************************************\n'


def escape(string):
    return string.replace('(', '\(').replace(')', '\)').replace(' ', '\ ')


def getFinalScore(scores, casesPath):
    weightsFile = casesPath + 'weights.txt'
    if os.path.exists(weightsFile):
        weights = [int(w) for w in open(weightsFile)]
    else:
        # Uniform weighting of cases
        weights = [100/float(len(scores))] * len(scores)
        weights[-1] += (100 - sum(weights))

    total = 0

    assert len(weights) == len(scores)
    assert sum(weights) == 100.0

    for i in xrange(len(scores)):
        total += scores[i] * weights[i]

    return total / 100


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Judge a C/++ program on a set of test data.')
    parser.add_argument('path_to_cases',
        help='Path to the directory of cases. Directory must have '
             'subdirectories in/ out/ and optionally a weights.txt. '
             'The nth test case has input file in/n.in and output out/n.out.')
    parser.add_argument(
        'in_file', help='the name of the input file read by the program')
    parser.add_argument(
        'out_file', help='the name of the output file read by the program')
    parser.add_argument(
        'source_file', help='path to the source code')
    parser.add_argument(
        '-t', '--time_limit', metavar="XX", type=float, default=1.0,
        help='set time limit of XXs per test case (default 1)')

    args = parser.parse_args()

    compileAndJudge(args.source_file, args.in_file, args.out_file,
                    args.path_to_cases, args.time_limit)
