import sys
import re

class concord:

    def __init__(self, input=None, output=None):
        self.input = input
        self.output = output
        if(self.input != None or self.output != None) :
            self.full_concordance()
        # self.determine_index_words()

    def full_concordance(self):
    	 #the list that holds all exclusion words
        exclusion = []
    #the list that contains the lines for index
        indexlines = []
    #a trigger that decides when the input switches from exclusion too lines for index
        notexclude = 0
        if(self.input == None ):
            for line in sys.stdin:
                if re.match(" *\n$", line):
                    continue
                line = re.sub(' *\n$', '', line)
        #case that a test from assignment one is input
                if line == "1": 
                    print("Input is version 1, concord2.py expected version 2")
                    return
                if line == "2" or line == "''''":
                    continue
                if line == "\"\"\"\"":
                    notexclude = 1
                    continue
                if notexclude == 0:
                    exclusion.append(line)      
                if notexclude == 1:
                    indexlines.append(line)
                
        else:
            inputfile = open(self.input, 'r')
            for line in inputfile:
                if re.match(" *\n$", line):
                    continue
                line = re.sub('\n', '', line)
        #case that a test from assignment one is input
                if line == "1": 
                    print("Input is version 1, concord2.py expected version 2")
                    return
                if line == "2" or line == "''''":
                    continue
                if line == "\"\"\"\"":
                    notexclude = 1
                    continue
                if notexclude == 0:
                    exclusion.append(line)      
                if notexclude == 1:
                    indexlines.append(line)
            inputfile.close()        
        
    #a list that contain a touple for each line that has all necessary sorting and line spacing information
        tuplelist = [] 
       
        for line in indexlines:
            i = 0
            firstcap = 0
            linewords = re.split(" ", line)
            for word in linewords:
                ignore = 0
            #decides wether a word is an exclusion word or not
                for exclude in exclusion:
                    if word == exclude or word.lower() == exclude:
                        ignore = 1
                if ignore == 0:
                    cpy = linewords[:]
                    capword = word.upper()
                    cpy.pop(i)
                    if i < len(cpy):
                        cpy.insert(i, capword)
                    else:
                        cpy.append(capword)
                    cpy = " ".join(cpy)
                #a tuple is input into tuplelist that contains the word to sort by, the line with capitalized word, the length of the line, and the index of the first cap
                    tuplelist.append((word.lower(),cpy,len(line),firstcap))
                firstcap = firstcap + len(word)+1
                i = i+1
    #a function that sorts the list by the first part of the tuplr which is the word to sort by
        tuplelist.sort(key = lambda x: x[0])
 
        i = 0;
        for info in tuplelist:
        #loop that cuts off the first word of the sentence if its too long and reevaluates until it is short enough
            while info[3]-1 > 19:
                cutline = re.split(" ", info[1])
                removelength = len(cutline[0])+1
                cutline.pop(0)
                cutline = " ".join(cutline)
                tuplelist[i] = (info[0], cutline, len(cutline), info[3] - removelength)
                info = (info[0], cutline, len(cutline), info[3] - removelength)
        #loop that cuts from the end until its the correct length 
            while info[2] - info[3] > 31:
                cutline = re.split(" ", info[1])
                cutline.pop(len(cutline)-1)
                cutline = " ".join(cutline)
                tuplelist[i] = (info[0], cutline, len(cutline),info[3])
                info = (info[0], cutline, len(cutline), info[3]) 
            i = i+1

    #print out all the sentences with the correct amount of spaces at the front to a line the sentences with the 30th column
        if(self.input == None):
            output = []
            for word in tuplelist:
                output.append((" " * (29-word[3])) + word[1])
            return output
        else:
            outputfile = open(self.output, 'w')
            for word in tuplelist:
                outputfile.write((" " * (29-word[3])) + word[1] + "\n")
            outputfile.close()
            return []
