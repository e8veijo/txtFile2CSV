# Python program to remove specific lines from a text file

import sys, getopt, re

def list_help():
    print('Usage: del_line.py: [OPTION]... [FILE]...')
    print('delete lines in a file with key string and/or regex.')
    print('+----------------------------------------------------------------+')
    print('! First:  Delete lines with keyword,                             !') 
    print('!         thats good for page headers/footers...                 !')
    print('! Second: Delete lines with REGEX (regular expressions),         !') 
    print('!         example: "ID ([0-9][0-9][0-9])"                        !')
    print('+----------------------------------------------------------------+')
    print('-s --String  DELETE LINE keyword, case sensitive')
    print('-r --Regex   DELETE LINE regular expresion')
    print('-t --Test    Test the key and count the matching lines ')
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
    
    options = "s:r:ti:o:h"
    long_options = ["String=", "Regex=", "Test", "Input=", "Output=","Help", ]
    
    in_file     = ''
    out_file    = ''
    str_val     = ''
    reg_val     = ''
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
                print("Load help instructions")
                list_help()
                
            elif argument in ("-s", "--String"):
                print('String: ', value)
                str_val = value
                 
            elif argument in ("-r", "--Regex"):
                print("Regex: ", value)
                reg_val = value
            
            elif argument in ("-t", "--Test"):
                print("Test delete string")
                bol_test = True
                
            elif argument in ("-i", "--Input"):
                print("Input file: ",value)
                in_file = value
                
            elif argument in ("-o", "--Output"):
                print("Output file: ",value)
                out_file = value
                
    except getopt.error as err:
        print (str(err),'\n')
        list_help()
    
    if str_val or reg_val:
        i_lines = read_lines(in_file)
        o_lines = []
        del_k   = 1
        line_hit = False
        
        # First thing we do is STRING DELETE with keyword, good use for page numbers page headers/footers
        # Second thing we do is REGEX DELETE, example "ID ([0-9][0-9][0-9][0-9][0-9][0-9])"
        for line in i_lines:
            if str_val and str_val in line: 
                line_hit = True
            if reg_val and re.match(reg_val, line) != None:
                line_hit = True
                
            if line_hit:
                if bol_test: # Add key hit to output
                    txt = "::::: DELETED LINE NO " + str(del_k) + " ::::: " + line
                    #print(txt)
                    o_lines.append(txt)
                    del_k += 1
                else:
                    #print('removed a line', del_k)
                    del_k += 1
            else:
                if not bol_test:
                    o_lines.append(line)
                
            line_hit = False
            
        if bol_test:
            o_lines.append('\nATT: Summary, deleted ' + str(del_k - 1) + ' line(s)\n')
            if del_k == 1:
                o_lines.append('Please try other key!')
                
        if out_file: # Result -> file
            with open(out_file,'w') as output:
                for oline in o_lines:
                    output.write(oline)
            print('\nATT: Summary, deleted ' + str(del_k - 1) + ' line(s)\n')
            if del_k == 1:
                print('Please try other key!')
        else:
            for oline in o_lines:
                print(oline.strip('\n'))
                

    else:
        list_help()

if __name__ == "__main__":
    main()