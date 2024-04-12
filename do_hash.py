# Python program to remove specific lines from a text file

import sys, getopt, re

def list_help():
    print('Usage: do_hash.py: [OPTION]... [FILE]...')
    print('Extract hash output list from a text file using begin/end keys.')
    print(' Begin key will be hash key with content lines from begin to end.')
    print('+--------------------------------------------------------------+')
    print('! First:   String keys are used to create hash table output    !') 
    print('! Second:  REGEX (regular expressions),                        !') 
    print('!          example: "ID ([0-9][0-9][0-9])"                     !')
    print('+--------------------------------------------------------------+')
    print('-a --Start   String begin keyword')
    print('-b --Stop    String stop keyword')
    print('-c --Begin   Regex begin  key')
    print('-d --End     Regex end  key')
    print('-t --Test    Test the keys and count the matching lines')
    print('-v --Sepa    Separator symbol, default is semicolon ;')
    print('-i --Input   input file, MANDATORY')
    print('-o --Output  output file, if empty -> STD output')
    print('-h --Help    list command information')
    sys.exit()

def read_lines(filename):
    lines = []
    with open(filename, 'r') as fp:
        lines = fp.readlines()
    return lines
        
def main():
    # Remove 1st argument from the list of command line arguments
    argumentList = sys.argv[1:]
    #print("argumentList:", argumentList)
    
    options = "a:b:c:d:tv:i:o:h"
    long_options = ["Start="," Stop=", "Begin=", "End=", "Test", "Sepa=", "Input=", "Output=","Help", ]
    
    in_file     = ''
    out_file    = ''
    str_start   = ''
    str_stop    = ''
    reg_begin   = ''
    reg_end     = ''
    str_sep     = ';'
    bol_test    = False
    
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        #print("arguments:   ",arguments)
        #print("values:      ",values)
        
        if not len(arguments) > 0:
            list_help()
        
        for argument, value in arguments:
            #print("current Argument: ", argument)
            #print("current Value:    ", value)
                
            if argument in ("-h", "--Help"):
                print("Help, help")
                list_help()
                
            elif argument in ("-t", "--Test"):
                print("Test")
                bol_test = True
            
            elif argument in ("-a", "--Start"):
                print("Start string: ", value)
                str_start = value
                
            elif argument in ("-b", "--Stop"):
                print("Stop string: ", value)
                str_stop = value
          
            elif argument in ("-c", "--Begin"):
                print("Regex begin: ", value)
                reg_begin = value
            
            elif argument in ("-d", "--End"):
                print("Regex end: ", value)
                reg_end = value
                
            elif argument in ("-v", "--Sepa"):
                print("Separator string: ", value)
                str_sep = value
                
            elif argument in ("-i", "--Input"):
                print("Input file: ",value)
                in_file = value
                
            elif argument in ("-o", "--Output"):
                print("Output file: ",value)
                out_file = value
                
    except getopt.error as err:
        print (str(err),'\n')
        list_help()
                        
    if ( ( str_start and str_stop ) or
         ( reg_begin and reg_end )
       ):
        i_lines = read_lines(in_file)
        o_lines = []
        l_cnt   = len(i_lines)
        k_start = 0
        k_stop  = 0
        i_start = 0
        i_stop  = 0
        
        for i in range(0, l_cnt):
            if str_start: # use strings to filter
                if k_start == 0 and str_start in i_lines[i]:
                    i_start += 1
                    k_start = i
                    #print("START STRING FOUND: " + str(k_start) + ' ::::: ' + i_lines[k_start].strip('\n'))
                    
                elif k_start > 0 and str_stop in i_lines[i]:
                    i_stop += 1
                    k_stop = i
                    #print("STOPP STRING FOUND: " + str(k_stop) + ' ::::: ' + i_lines[k_stop].strip('\n'))
                    
            else: # use regex to filter
                if k_start == 0 and re.match(reg_begin, i_lines[i]) != None:
                    k_start = i
                    i_start += 1
                    #print("START REGEX FOUND: " + str(k_start) + ' ::::: ' + i_lines[k_start].strip('\n'))
                elif k_start > 0 and re.match(reg_end, i_lines[i]) != None:
                    k_stop = i
                    i_stop += 1
                    #print("STOP REGEX FOUND:  " + str(k_stop) + ' ::::: ' + i_lines[k_stop].strip('\n'))
                
            if k_start > 0 and k_stop > 0:
                if bol_test: # Add keys matching lines to output
                    o_lines.append("START: " + str(k_start) + ' : ' + i_lines[k_start])
                    o_lines.append("STOP:  " + str(k_stop)  + ' : ' + i_lines[k_stop])
                else:
                    o_lines.append(str_sep + '\n')                  # Separator
                    o_lines.append(i_lines[k_start])                # Hash key
                    o_lines.append(str_sep + '\n')                  # Separator
                    for j in range(k_start, k_stop):
                        o_lines.append(i_lines[j])                  # Data
                
                stop_is_new_start = False
                
                if str_start: # use strings to filter
                    stop_is_new_start = str_start == str_stop
                    
                else: # use regex to filter
                    stop_is_new_start = reg_begin == reg_end
                    
                if stop_is_new_start: # if start and stop are equal, then stop is new start
                    k_start  = k_stop
                    k_stop   = 0
                    i_start += 1
                    #print('STOP is recognized as new START')
                else:
                    k_start = 0
                    k_stop  = 0
                
        if bol_test or not out_file:
            o_lines.append('\nATT: Summary, start key(s) found: ' + str(i_start) + '\n')
            o_lines.append('\nATT: Summary, stop key(s) found:  ' + str(i_stop) + '\n')
            if i_start == 0 or i_stop == 0:
                o_lines.append('Please try other keys!')
            
        if out_file: # Result -> file
            with open(out_file,'w') as output:
                for oline in o_lines:
                    output.write(oline)
                    
            print('\nATT: Summary, start key(s) found: ' + str(i_start))
            print('\nATT: Summary, stop key(s) found:  ' + str(i_stop))
            if i_start ==0 or i_stop == 0:
                print('Please try other keys!')
        else:
            for oline in o_lines:
                print(oline.strip('\n'))
        
            
if __name__ == "__main__":
    main()

