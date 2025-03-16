import csv


with open('bgp_rib.csv', 'r') as bgp_file:
    bgp_reader = csv.DictReader(bgp_file,delimiter=";")
    bgp_data = list(bgp_reader)
    
print("Number of BGP RIBs: {}".format(len(bgp_data)))
print()
print("Sample BGP RIB: {}".format(bgp_data[0]))

longestASPATH = []
longestSoFar = 0
for entry in bgp_data:
    temp = []
    tempCount = 0
    for number in entry['ASPATH'].split(' '):
        if(number not in temp):
            tempCount += 1
        temp.append(number)
    if(tempCount > longestSoFar):
        longestASPATH = temp
        longestSoFar = tempCount

print()
print("longest path")
print(longestASPATH)

bgp_36992 = []
for entry in bgp_data:
    path = entry['ASPATH'].split(' ')
    if(path[-1] == '36992'):
        bgp_36992.append(entry)
        print(entry)
fieldnames = ['TIME','ORIGIN','FROM','SEQUENCE','ASPATH','PREFIX','NEXT_HOP']
with open('bgp_36992.csv', 'w') as bgp2_file:
    bgp_writer = csv.DictWriter(bgp2_file,fieldnames=fieldnames,delimiter=";")
    bgp_writer.writerows(bgp_36992)