#!/usr/bin/env python

# pylint: disable=C0103, C0111, C0301, R0903, W0622, W0621, W0603

r"""
A large stream blocks your path. According to the locals, it's not safe to
cross the stream at the moment because it's full of garbage. You look down at
the stream; rather than water, you discover that it's a stream of characters.

You sit for a while and record part of the stream (your puzzle input). The
characters represent groups - sequences that begin with { and end with }.
Within a group, there are zero or more other things, separated by commas:
either another group or garbage. Since groups can contain other groups, a }
only closes the most-recently-opened unclosed group - that is, they are
nestable. Your puzzle input represents a single, large group which itself
contains many smaller ones.

Sometimes, instead of a group, you will find garbage. Garbage begins with < and
ends with >. Between those angle brackets, almost any character can appear,
including { and }. Within garbage, < has no special meaning.

In a futile attempt to clean up the garbage, some program has canceled some of
 the characters within it using !: inside garbage, any ONE character that comes
 after ! should be ignored, including <, >, and even another !.

You don't see any characters that deviate from these rules. Outside garbage,
you only find well-formed groups, and garbage always terminates according to
the rules above.

Here are some self-contained pieces of garbage:

<>, empty garbage.
<random characters>, garbage containing random characters.
<<<<>, because the extra < are ignored.
<{!>}>, because the first > is canceled.
<!!>, because the second ! is canceled, allowing the > to terminate the garbage.
<!!!>>, because the second ! and the first > are canceled.
<{o"i!a,<{i<a>, which ends at the first >.
Here are some examples of whole streams and the number of groups they contain:

{}, 1 group.
{{{}}}, 3 groups.
{{},{}}, also 3 groups.
{{{},{},{{}}}}, 6 groups.
{<{},{},{{}}>}, 1 group (which itself contains garbage).
{<a>,<a>,<a>,<a>}, 1 group.
{{<a>},{<a>},{<a>},{<a>}}, 5 groups.
{{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).

Your goal is to find the total score for all groups in your input. Each group
is assigned a score which is one more than the score of the group that
immediately contains it. (The outermost group gets a score of 1.)

{}, score of 1.
{{{}}}, score of 1 + 2 + 3 = 6.
{{},{}}, score of 1 + 2 + 2 = 5.
{{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
{<a>,<a>,<a>,<a>}, score of 1.
{{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
{{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
{{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.
"""

import fileinput
from collections import defaultdict
SCORE = 0
STACK = 0
CANCEL = False
GARBAGE = False
GARBAGE_COUNT = 0


def canceller(f):
    def g():
        global CANCEL
        if CANCEL:
            CANCEL = False
            return
        return f()
    return g


@canceller
def in_stack():
    global STACK, GARBAGE, GARBAGE_COUNT
    if not GARBAGE:
        STACK += 1
    else:
        GARBAGE_COUNT += 1


@canceller
def out_stack():
    global STACK, SCORE, GARBAGE, GARBAGE_COUNT
    if not GARBAGE:
        SCORE += STACK
        STACK -= 1
    else:
        GARBAGE_COUNT += 1


@canceller
def in_garbage():
    global GARBAGE, GARBAGE_COUNT
    GARBAGE_COUNT += 1 if GARBAGE else 0
    GARBAGE = True


@canceller
def out_garbage():
    global GARBAGE
    GARBAGE = False


@canceller
def saw_canceller():
    global CANCEL, GARBAGE
    CANCEL = True if GARBAGE else False

@canceller
def otro():
    global GARBAGE_COUNT
    GARBAGE_COUNT += 1 if GARBAGE else 0

LU = defaultdict(lambda: otro,
                 {
                     "{": in_stack,
                     "}": out_stack,
                     "<": in_garbage,
                     ">": out_garbage,
                     "!": saw_canceller
                 })
for char in fileinput.input().readline().strip():
    LU[char]()
print GARBAGE_COUNT
