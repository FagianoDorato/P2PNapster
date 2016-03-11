import json
import os
from modules.SharedFile import SharedFile
import hashlib

# Helper Methods
def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()[:16]


def fileExists(list,md5):
	for l in list:
		if l.md5.lower() == md5.lower():
			return True


class Peer(object):
	SessionId = ""
	Ipv4 = "172.30.8.1"
	Ipv6 = "fc00::8:1"
	Port = "3000"
	filesList = []

	def __init__(self):
		# Loading file list
		listFile = open('list.txt','w+')
		result = listFile.read()

		if not result == "":
			files = json.loads(result)
			for f in files:
				obj = SharedFile(f["name"],f["md5"],f["shared"])
				self.filesList.append(obj)

		# print("List of available files:")
		# Searching for new sharable
		for root, dirs, files in os.walk("sharable"):
			for file in files:
				fileMd5 = hashfile(open("sharable/" + file, 'rb'), hashlib.md5())
				if not fileExists(self.filesList, fileMd5):
					# File doesn't exist adding to the list
					newFile = SharedFile(file,fileMd5,"false")
					self.filesList.append(newFile)
				else:
					print("file already exist!")


		# Saving list
		listFile.write(json.dumps([o.dump() for o in self.filesList]))

	def login(self):
		# TODO: Log in and return sessionId
		self.SessionId = "ashbnvdujghb"

	def logout(self):
		# TODO: Log out
		self.SessionId = ""
		return

	def share(self):
		print("Select a file to share")
		for idx, file in enumerate(self.filesList):
			if file.shared == "false":
				print(str(idx) + ": " + file.name)
		option = input()

		for idx, file in enumerate(self.filesList):
			if idx == int(option):
				print("Adding file " + file.name)
				# TODO: add file
				formatSend="ADDF"+self.SessionId+file.md5+file.name

				# TODO: modify file shared status in list.txt
				file.shared = "true"
				print("done")


	def remove(self):
		print("Select a file to remove")
		for idx, file in enumerate(self.filesList):
			if file.shared == "true":
				print(str(idx) + ": " + file.name)
		option = input()

		for idx, file in enumerate(self.filesList):
			if idx == int(option):
				print("Removing file " + file.name)
				# TODO: remove file
				for root, dirs, files in os.walk("sharable"):
					for file in files:
						fileMd5 = hashfile(open("sharable/" + file.name, 'rb'), hashlib.md5())
						#if file exist already, delete it
						if fileExists(self.filesList, fileMd5):
							self.filesList.remove(file.name)
				# TODO: modify file shared status in list.txt
				print("Done")

	def search(self):
		print("Insert search term:")
		term = input()

		print("Searching files that match: "+ term)
		# TODO: search files
		availableFiles = []
		self.download(availableFiles)

	# availableFiles è una lista recuperata tramite la ricerca che contiene i risultati
	def download(self, availableFiles):
		# visualizza i risultati della ricerca
		print("Select a file to download: ")
		print("lista file...")
		# seleziona un file da scaricare

		# visualizza la lista dei peer da cui è possibile scaricarlo
		print("Select a peer: ")
		print("lista peer con indirizzi...")
		# seleziona un peer

		# download
		print("download")
