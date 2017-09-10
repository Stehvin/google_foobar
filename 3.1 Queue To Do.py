# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:56:49 2017

@author: Stehvin
"""

'''
Queue To Do
===========

You're almost ready to make your move to destroy the LAMBCHOP doomsday 
device, but the security checkpoints that guard the underlying systems of 
the LAMBCHOP are going to be a problem. You were able to take one down 
without tripping any alarms, which is great! Except that as Commander 
Lambda's assistant, you've learned that the checkpoints are about to come 
under automated review, which means that your sabotage will be discovered 
and your cover blown - unless you can trick the automated review system.

To trick the system, you'll need to write a program to return the same 
security checksum that the guards would have after they would have checked 
all the workers through. Fortunately, Commander Lambda's desire for 
efficiency won't allow for hours-long lines, so the checkpoint guards have 
found ways to quicken the pass-through rate. Instead of checking each and 
every worker coming through, the guards instead go over everyone in line 
while noting their security IDs, then allow the line to fill back up. Once 
they've done that they go over the line again, this time leaving off the 
last worker. They continue doing this, leaving off one more worker from the 
line each time but recording the security IDs of those they do check, until 
they skip the entire line, at which point they XOR the IDs of all the 
workers they noted into a checksum and then take off for lunch. Fortunately, 
the workers' orderly nature causes them to always line up in numerical order 
without any gaps.

For example, if the first worker in line has ID 0 and the security 
checkpoint line holds three workers, the process would look like this:

0 1 2 /
3 4 / 5
6 / 7 8

where the guards' XOR (^) checksum is 0^1^2^3^4^6 == 2.

Likewise, if the first worker has ID 17 and the checkpoint holds four 
workers, the process would look like:

17 18 19 20 /
21 22 23 / 24
25 26 / 27 28
29 / 30 31 32

which produces the checksum 17^18^19^20^21^22^23^25^26^29 == 14.

All worker IDs (including the first worker) are between 0 and 2000000000 
inclusive, and the checkpoint line will always be at least 1 worker long.

With this information, write a function answer(start, length) that will 
cover for the missing security checkpoint by outputting the same checksum 
the guards would normally submit before lunch. You have just enough time to 
find out the ID of the first worker to be checked (start) and the length of 
the line (length) before the automatic review occurs, so your program must 
generate the proper checksum with just those two values.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) start = 0
    (int) length = 3
Output:
    (int) 2

Inputs:
    (int) start = 17
    (int) length = 4
Output:
    (int) 14

Use verify [file] to test your solution and see how it does. When you 
are finished editing your code, use submit [file] to submit your 
answer. If your solution passes the test cases, it will be removed 
from your home folder.
'''

def answer(start, length):
    '''
    Inputs: start (int), beginning number in sequence
            length (int), length of line/iterations
    Outputs: checksum (int), correct output of the guard's
        XOR checksum
    '''
    
    #Initialize variables
    endNum = start + (length * (length - 1))
    counter = 0
    bitString = ""
    first = start
    
    # Get max num of bits
    while endNum:
        counter += 1
        endNum = endNum >> 1
    
    # Iterate over bits to find number of odds
    for i in range(0, counter):
    
        # Get sequence length
        seqLen = 2**i
        
        # Get first even or odd
        modFirst = first % 2
        
        # Get sequence index of first number
        indFirst = start % (2**i)
        
        numOdds = 0
        
        # Iterate over rows
        for i2 in range(0, length):
          
            # Initialize variables for number of odds calculation
            rowLen = float(length - i2)
            numSeq = rowLen / seqLen
            var1 = (numSeq // 2)*2
            var2 = numSeq - var1
            numFirstTypeClean = (var1 / 2)*seqLen
            positionsLeft = var2 * seqLen
            
            # Get number of evens or odds in row
            if positionsLeft - (seqLen - indFirst) < 0:
                numFirstTypeDirty = positionsLeft
            elif positionsLeft - (seqLen - indFirst) <= seqLen:
                numFirstTypeDirty = seqLen - indFirst
            else:
                numFirstTypeDirty = (seqLen - indFirst) + \
                                    (positionsLeft - (2*seqLen) + indFirst)
            
            numFirstType = numFirstTypeDirty + numFirstTypeClean
            
            # Check if first number is odd
            if modFirst == 1:
                numOdds += numFirstType
            else:
                numOdds += rowLen - numFirstType
            
            # Check if next row's first number is odd
            if (indFirst + length) % (2*seqLen) >= seqLen:
                modFirst = (modFirst + 1) % 2
            
            # Check next row's intial sequence index
            indFirst = (indFirst + length) % seqLen
        
        # Convert number of odds into a bit
        bitString = str(int(numOdds % 2)) + bitString
        first = first // 2
    
    checksum = int(bitString, 2)
    return checksum