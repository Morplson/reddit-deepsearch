from builtins import input
import urllib
from urllib.parse import unquote
import re
import argparse
import threading
import math
import pandas


parser = argparse.ArgumentParser(description='Analyse SQL injection attempts in web server logs')

#Input and Output
parser.add_argument('-f', '--file',  help='Input file to process')
parser.add_argument('-o', '--output',  help='Output file to write to')

#Filtering
parser.add_argument('-x', '--filter', action='store_true', help='Filters by ip, time or user_agent')

#Routines
parser.add_argument('-i', '--info', action='store_true', help='Shows request infos')
parser.add_argument('-r', '--readable', action='store_true', help='Reverse Urlencode')
parser.add_argument('-d', '--deobfuscate', action='store_true', help='Trys to deobfuscate the requests')
parser.add_argument('-t', '--tables', action='store_true', help='Guesses fetched data')
parser.add_argument('-g', '--guess', action='store_true', help='Guesses fetched data')

#Settings
parser.add_argument('-e', '--experimental', action='store_true', help='Enable experimental deobfuscation techniques(Substring)')
parser.add_argument('-v', '--vebrose', action='store_true', help='Additional information while executing')

#App Info
parser.add_argument('-V', '--version', action='store_true', help='Show app info')
args = parser.parse_args()

banner = r'''
  _______ _  _____ _______ ___ __ _  ___ ____ 
 / __/ -_) |/ / -_) __(_-</ -_)  ' \/ _ `/ _ \
/_/  \__/|___/\__/_/ /___/\__/_/_/_/\_,_/ .__/
        Remastered v0.1                /_/      
'''


def version():
    print("""
    Reversemap is used to analyse SQL injection attempts in web server logs

    """)




#info
def info_batcher(data):
    results = []

    thread_num = 4

    if len(data)>0:
        class_size = math.ceil(len(data)/thread_num)
        classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]

        threads = []
        for i in range(len(classes)):
            results.append([])
            thread = threading.Thread(target=readable, args=(classes[i],results[i], ))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    results = [item for sublist in results for item in sublist]



def info(batch_data, results):
    for line in batch_data:
        res = {"ip":None, "useragent":None, "time":None}

        ip = re.search(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', line, re.IGNORECASE)

        results.append(res)



#readable
def readable_batcher(data):
    results = []

    thread_num = 4

    if len(data)>0:
        class_size = math.ceil(len(data)/thread_num)
        classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]

        threads = []
        for i in range(len(classes)):
            results.append([])
            thread = threading.Thread(target=readable, args=(classes[i],results[i], ))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    results = [item for sublist in results for item in sublist]
    return results

def readable(batch_data, results):
    for x in batch_data:
        decodedurl = unquote(x)
        decodedurl = decodedurl.replace('/**/', '')

        results.append(decodedurl)



def deobfuscate(input):
    sqlkeywords = ['SELECT ', 'DISTINCT ', 'FROM ', 'WHERE ', 'CAST\(', 'CONVERT\(', 'ORDER ', 'BY ', 'AS ', 'ON ', 'JOIN ', '@@VERSION', ' ASC', ' LIKE ', ' TOP ', ' AND ', ' DESC', ' SQ ', 'UNION ', 'CHAR\(', 'VERSION\(\)', 'ALL ']
    return







if __name__ == "__main__":
    print(banner)

    if args.help:
        info()

    
    
    
    #Functionality 
    elif args.file is not None and args.output is not None:
        print(args.file)
        f = open(str(args.file), "r")
        out = open(str(args.output), "w")
        out.write("")
        out.close()
        out = open(str(args.output), "a")


        #Batched Opperations 
        data = f.readlines()



    #Help
    else:
        parser.print_help()