#!/usr/bin/env python

import socket

def recv_until(conn, str):
	buf = ''
	while not str in buf:
		buf += conn.recv(1)
	return buf

def getValidSubnet(host):
	result = ""
	dot_counter = 0
	count = 0
	for c in host:
		if (dot_counter < 3):
			if (c == '.'):
				dot_counter = dot_counter + 1
		else:
			result = host[0:count]
			result = result + "0/24"			
			break
		count = count + 1
	return result

def countHosts(subnet):
	last1 = subnet[len(subnet)-1]
	last2 = subnet[len(subnet)-2]

	bindigit = 0
	if (last2 == '/'):
		bindigit = 32 - int(last1)
	else:
		bindigit = 32 - (int(last1)+int(last2)*10)

	num_of_server = 2**bindigit
	return str(num_of_server)

def isSubnetValid(subnet, host):
	last1 = subnet[len(subnet)-1]
	last2 = subnet[len(subnet)-2]
	bindigit = 0

	ans = "T"
	if (last2 == '/'):
		bindigit = int(last1)
		subnet_len = len(subnet)-2
	else:
		bindigit = (int(last1)+int(last2)*10)
		subnet_len = len(subnet)-3

	if (bindigit > 0):
		subnet = subnet[0:subnet_len]
		subnet_num_list = subnet.split(".")
		host_num_list = host.split(".")
	
		subnetInt = 2**24 * int(subnet_num_list[0]) + 2**16 * int(subnet_num_list[1]) + 2**8 * int(subnet_num_list[2]) + int(subnet_num_list[3])
		hostInt = 2**24 * int(host_num_list[0]) + 2**16 * int(host_num_list[1]) + 2**8 * int(host_num_list[2]) + int(host_num_list[3])
	
		if (subnetInt ^ hostInt < 2**(32-bindigit)):
			ans = "T"
		else:
			ans = "F"
	
	return ans
	
TCP_IP = 'hmif.cf'
TCP_PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

data = recv_until(s, 'NIM: ')
nim = raw_input(data)
s.send(nim + '\n')

data = recv_until(s, 'Verify NIM: ')
nim = raw_input(data)
s.send(nim + '\n')

print recv_until(s, '\n')[:-1]

# Phase 1
for i in range(100):
	recv_until(s, 'Host: ')
	host = recv_until(s, '\n')[:-1]
	recv_until(s, 'Subnet: ')
	s.send(getValidSubnet(host) + '\n')
print recv_until(s, '\n')[:-1]

# Phase 2
for i in range(100):
	recv_until(s, 'Subnet: ')
	subnet = recv_until(s, '\n')[:-1]
	recv_until(s, 'Number of Hosts: ')
	s.send(countHosts(subnet) + '\n')
print recv_until(s, '\n')[:-1]

# Phase 3
for i in range(100):
	recv_until(s, 'Subnet: ')
	subnet = recv_until(s, '\n')[:-1]
	recv_until(s, 'Host: ')
	host = recv_until(s, '\n')[:-1]
	s.send(isSubnetValid(subnet, host) + '\n')
print recv_until(s, '\n')[:-1]

s.close()
