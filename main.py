#libraries

#modules
from modules.Peer import Peer


# program flow
# Peer initialization
p = Peer()


while p.SessionId == "":
	print("Select one of the following options:")
	print("1: Log In")
	option = input()
	if option != "1":
		print(option + " not recognized as a command")
	else:
		print('Logging in...')

		# TODO: Login
		p.login()
		print('Completed.')

		while 1:
			print("Select one of the following options:")
			print("1: Add File")
			print("2: Remove File")
			print("3: Search File")
			print("4: LogOut")

			option = input()

			if option == "1":
				p.share()
			elif option == "2":
				p.remove()
			elif option == "3":
				p.search()
			elif option == "4":
				p.logout()
			else:
				print(option + " not recognized as a command")