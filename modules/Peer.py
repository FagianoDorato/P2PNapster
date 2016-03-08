import json
import os
from modules.SharedFile import SharedFile
import hashlib

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

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
		#Loading file list
		listFile = open('list.txt','r+')
		result = listFile.read()
		files = json.loads(result)
		for f in files:
			obj = SharedFile(f["name"],f["md5"],f["shared"])
			self.filesList.append(obj)

		#print("List of available files:")
		#Searching for new sharable
		for root, dirs, files in os.walk("sharable"):
			for file in files:
				fileMd5 = hashfile(open("sharable/" + file, 'rb'), hashlib.md5())
				if not fileExists(self.filesList, fileMd5):
					#File doesn't exist adding to the list
					newFile = SharedFile(file,fileMd5,"false")
					self.filesList.append(newFile)


		#Saving list
		listFile.write(json.dumps([o.dump() for o in self.filesList]))


