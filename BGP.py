import csv


with open('bgp_rib.csv', 'r') as bgp_file:
    bgp_reader = csv.DictReader(bgp_file,delimiter=";")
    bgp_data = list(bgp_reader)
    
print("Number of BGP RIBs: {}".format(len(bgp_data)))
print()
print("Sample BGP RIB: {}".format(bgp_data[0]))

longestASPATH = ''
for entry in bgp_data:
    if(entry['ASPATH'].__len__() > longestASPATH.__len__()):
        longestASPATH = entry['ASPATH']
print(longestASPATH)