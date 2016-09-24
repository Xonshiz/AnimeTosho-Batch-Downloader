#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "Xonshiz"
__email__ = "xonshiz@psychoticelites.com"
__website__ = "http://www.psychoticelites.com"
__version__ = "v2.0"

'''


Script Info :

Author : Xonshiz
Github : https://github.com/Xonshiz
Twitter : twitter.com/Xonshiz
Website : http://www.psychoticelites.com
Email ID: xonshiz@psychoticelites.com

'''





"""
#############################################################################################################
# 										FEATURES :															#
#############################################################################################################
#																											#
# 1.) Downloads Episodes/Batches listed on AnimeTosho. 														#
# 2.) Uses SolidFiles to download files from. 																#
# 3.) Puts the downloaded files in a folder named 'Output'. 												#
# 4.) Skips the file if it already exists in the path. 														#
#																											#
#############################################################################################################
# 										FUTURE FEATURES :													#
#############################################################################################################
#																											#
# 1.) Be able to download from some other host, if the file isn't available on SolidFiles 					#
# 2.) Ability to let the user choose which episodes to download from a batch								#
#																											#
#############################################################################################################
# 										CHANGELOG :															#
#############################################################################################################
#																											#
# 1.) Re-Wrote the whole script for better understanding and flow. 											#
# 2.) Everything from AnimeTosho can be downloaded. (Homepage, Batches, Single Episodes)					#
# 4.) File skipping, if the file already exists. 															#
#																											#
#############################################################################################################

"""

from bs4 import BeautifulSoup
import urllib2,sys,re,shutil,urllib,os,subprocess,requests,time



def SolidFiles_Downloader(url):
	#pass

	#print 'Inside SolidFiles DLr'
	Current_Directory = os.getcwd()
	#print Current_Directory
	if not os.path.exists('Output'):
		os.makedirs('Output')

	r= requests.get(url)
	#print r.text
	with open('.temp_file','w') as sf:
		sf.write(str(r.text.encode('utf-8')))
		sf.flush()
	sf.close

	with open('.temp_file') as searchfile:
		for line in searchfile:
			left,sep,right = line.partition('"download_url":')
			if sep:
				#print sep
				OG_Title = right
				#print OG_Title
				Splitter = OG_Title.split('}')
				DL_Link = str(Splitter[0]).replace('"','').strip()
				#print DL_Link

	with open('.temp_file') as searchfile:
		for line in searchfile:
			left,sep,right = line.partition('"name":')
			if sep:
				#print sep
				OG_Title = right
				#print OG_Title
				Splitter = OG_Title.split(',')
				File_Name = str(Splitter[0]).replace('"','').strip()
				#print File_Name

	Output_Path = os.path.join(os.getcwd(), 'Output')
	Final_File_Path = os.path.join(Output_Path, File_Name)
	# Final_File_Path = str(Current_Directory)+'\Output\\'+File_Name
	# print Final_File_Path

	current_File_Path = os.path.join(os.getcwd(),File_Name)
	File_Path = os.path.normpath(File_Name)

	if os.path.exists(current_File_Path):
		print 'Moving The File!'
		try:
			shutil.move(File_Path,Output_Path)
			pass
		except Exception, e:
			#raise e
			print e
			sys.exit()

	if os.path.exists(Final_File_Path):
		print File_Name,"Already Exists! Skipping it!"
		pass

	if not os.path.exists(Final_File_Path):
		u = urllib2.urlopen(DL_Link)
		f = open(File_Name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s \nTotal Size (Bytes) = %s" % (File_Name, file_size)

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break
			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,
		f.close()

		#File_Path = os.path.normpath(File_Name)
		try:
			shutil.move(File_Path,'/Output')
		except Exception, e:
			#raise e
			print e
			pass

def Single_Page(LinkMain):
	page_source = urllib2.urlopen(LinkMain).read()
	soup = BeautifulSoup(page_source,"lxml")
	for link in soup.find_all('a'):
		All_Links = (link.get('href'))
		solid_links = re.findall(r'https?://(?:(?P<prefix>www|m)\.)?(?P<url>solidfiles\.com/v/)',str(All_Links))
		#print solid_links
		if solid_links:
			#print link.get('href')
			SolidFile_Link_single = str(link.get('href')).strip()
			url = SolidFile_Link_single
			SolidFiles_Downloader(url)


def main():

	print '\n'
	print '{:^80}'.format('################################################')
	print '{:^80}'.format('AnimeTosho Downloader')
	print '{:^80}'.format('Author : Xonshiz')
	print '{:^80}'.format('################################################\n')

	try:
		LinkMain = str(raw_input('Enter The URL of Series Issue :  '))
		print '\n'
		if not LinkMain:
			print "I need a URL to download from!"
			sys.exit()
		if LinkMain:
			Single_Page(LinkMain)
	except Exception, e:
		#raise e
		print e
		sys.exit()



if __name__ == "__main__":
	main()
