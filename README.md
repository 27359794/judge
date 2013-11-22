judge
=====

Written in ~2010.

Hassle-free (assuming you have the right OS, right Python version, etc...) judge for C/++. Compiles the code, runs it against a series of test cases and pretty-prints its score.



    antares: judge\ $ python judge.py cases/ addin.txt addout.txt addition.c

    +-------------------------------------------------------+
    | SOURCE FILE: addition.c
    | INPUT:       addin.txt
    | OUTPUT:      addout.txt
    | WEIGHTED:    False
    +-------------------------------------------------------+

    JUDGE
    CASES: Num | Score |       Reason      |   Time
           ----+-------+-------------------+----------
            #1 |  100  | correct           |   0.008s
            #2 |  100  | correct           |   0.008s
            #3 |   0   | incorrect         |   0.008s
            #4 |   0   | incorrect         |   0.008s
    Score for this submission: 50%

Supports evaluation time limits and custom test case weightings. Output format is modelled on the [orac](http://orac.amt.edu.au) judge.

    antares: judge\ $ python judge.py -h
    usage: judge.py [-h] [-t XX] path_to_cases in_file out_file source_file

    Judge a C/++ program on a set of test data.

    positional arguments:
      path_to_cases         Path to the directory of cases. Directory must have
                            subdirectories in/ out/ and optionally a weights.txt.
                            The nth test case has input file in/n.in and output
                            out/n.out.
      in_file               the name of the input file read by the program
      out_file              the name of the output file read by the program
      source_file           path to the source code

    optional arguments:
      -h, --help            show this help message and exit
      -t XX, --time_limit XX
                            set time limit of XXs per test case (default 1)

