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
count = 0
for entry in bgp_data:
    path = entry['ASPATH'].split(' ')
    if(path[-1] == '36992'):
        bgp_36992.append(entry)
        count +=1

print(f'num prefixes: {count}')
fieldnames = ['TIME','ORIGIN','FROM','SEQUENCE','ASPATH','PREFIX','NEXT_HOP']
with open('bgp_36992.csv', 'w') as bgp2_file:
    bgp_writer = csv.DictWriter(bgp2_file,fieldnames=fieldnames,delimiter=";")
    bgp_writer.writerows(bgp_36992)

rout_table = []
known_prefix = []
known_prefix_len = []
for entry in bgp_36992:
    prefix = entry['PREFIX']
    pfx, length = prefix.split('/')

    if pfx in known_prefix: # need to check if the length is shorter
        pindex = known_prefix.index(pfx)
        if(known_prefix_len[pindex] > length): # length is shorter update table
            known_prefix_len[pindex] = length
            rout_table[pindex]['PREFIX'] = prefix
            rout_table[pindex]['NEXT_HOP'] = entry['NEXT_HOP']
    else:
        tableEnt = {
            "DESTINATION" : '36992',
            "PREFIX" : prefix,
            "NEXT_HOP" : entry['NEXT_HOP']
        }
        known_prefix.append(pfx)
        known_prefix_len.append(length)
        rout_table.append(tableEnt)


fieldnames = ['DESTINATION','PREFIX','NEXT_HOP']
with open('forwarding-table.csv', 'w') as bgp3_file:
    bgp_writer = csv.DictWriter(bgp3_file,fieldnames=fieldnames,delimiter=";")
    bgp_writer.writerows(rout_table)