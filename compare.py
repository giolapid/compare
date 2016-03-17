#!usr/bin/env python

####################################################################################################
#
# compare.py
#
# Purpose: Compares men and mice IP addresses to IP360's.
# Takes in 2 input files containing IP addresses, subnets, and IP ranges.
# Then compares each indices of list A to list B. Returns duplicate values in the lists
#
# usage: python compare.py fileA(Men and Mice list) fileB(TripWire list)
#               
#
# Author: Gio Lapid
# 
# Growth Areas: argparse can be better by adding help
#
###################################################################################################

#Imports from python modules
import argparse
import ipaddr

#Parses the file and splits each string by ',' and returns a final list
#USE THIS FOR CSVS
def fileToListCSV(file):
	final_list = []
	with open(file,"r") as filestream:
		for line in filestream:
			current = line.split(",")
		filestream.close()
	for i in current:
		final_list.append(i.strip())
	return final_list

#USE FOR LINE SEPARATED IP addresses
def fileToList(file):
	initial_list=[]
	final_list =[]
	for line in open(file, "r" ).readlines():
	    for value in line.split(' '):
	        initial_list.append(value)
	for i in initial_list:
		final_list.append(i.strip())
	return final_list 

#Compares each index from file A to every index from file B
def compare(a,b):
        count = 0
        duplicates = []
	for i in range(len(a)):
		for x in range(len(b)):
                        if str(a[i]) == str(b[x]):
                                count += 1
                                duplicates.append(a[i])
                		f.write(str(a[i]) + " is a duplicate.\n")
        return duplicates, count

#Compares the masterlist to duplicates list and returns a list without duplicates
def removeDuplicates(masterlist, duplicates):
        a = list(masterlist)
        for i in range(len(masterlist)):
                for x in range(len(duplicates)):
                        if str(masterlist[i]) == str(duplicates[x]):
                                a.remove(duplicates[x])
                                break
        return a

#ipRange takes in starting IP and ending IP as input and puts the range into a list
def ipRange(start_ip, end_ip):
        start = list(map(int, start_ip.split(".")))
        end = list(map(int, end_ip.split(".")))
        temp = start
        ip_range = []
   
        ip_range.append(start_ip)
        while temp != end:
                start[3] += 1
                for i in (3, 2, 1):
                        if temp[i] == 256:
                                temp[i] = 0
                                temp[i-1] += 1
                ip_range.append(".".join(map(str, temp)))    
      
        return ip_range

#returns a list of IP ranges to a new list
def getDashList(masterlist):
        a = []
        for i in range(len(masterlist)):
                if '-' in masterlist[i]:
                        a.append(masterlist[i])
        return a

#uses the list from getDashList and turns them into a list of IPs in that range               
def rangeTolist(dashedlist):
        rangelist = []
        for i in range(len(dashedlist)):
                start = dashedlist[i].split('-')[0]
                end = dashedlist[i].split('-')[1]
                rangelist.extend(ipRange(start,end))
        return rangelist
                        
#uses ipaddr module to check if an IP is in the subnet returns a boolean
def inSubnet(subnet, ip):
        try:
                address = ipaddr.IPAddress(str(ip))
                network = ipaddr.IPNetwork(str(subnet))
                return network.Contains(address)
        except ValueError:                                
                pass
        
#uses inSubnet() to see if an IP is in the network
def inNetwork(a,b):
        count = 0
        for i in range(len(a)):
		for x in range(len(b)):
                        if inSubnet(a[i], b[x]):
                                f.write(str(b[x])+ " is a duplicate from subnet " + str(a[i]) + '\n')
                                count += 1
        return count
        
#Main function 
def main():
#Parses for files in the command line
	parser = argparse.ArgumentParser()
	parser.add_argument('file', nargs='+')
	args = parser.parse_args()
        file1 = args.file[0]
        file2 = args.file[1]
        
        print "Opening a file...."
        print "Running....\n"
#Adds the files to lists and compare       
        A = fileToList(file1)
        B = fileToList(file2)
        
#Lists the duplicates
	duplicates, count = compare(A,B)
	
#New lists removes the duplicates and will be passed into
	uniqueA = removeDuplicates(A,duplicates)
	dashedB = removeDuplicates(B,duplicates)
	
#Removes IPranges from the list
        dashed = getDashList(dashedB)
        uniqueB = filter(None,removeDuplicates(dashedB,dashed))
        
#Turns IPranges to a list and merges it to the masterlist
        uniqueB += rangeTolist(dashed)
      
#calls on the inNetwork method to see if IP is in the subnet and adds count
	count += inNetwork(uniqueA, uniqueB)
	print "DONE\n"
        print "There are " + str(count) + " duplicates. More info in the output file (out.txt).\n"

if __name__ == '__main__':
        f = open("out.txt", "w")
	main()
        f.close()
