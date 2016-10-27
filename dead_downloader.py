import urllib.request
import sys
import os

def get_and_save(url, folder):
	filename = url.rsplit('/', 1)[-1]
	path = folder + '/' + filename;

	print(url)

	try:
		response = urllib.request.urlopen(url)
		headers = response.info()
		d = dict(response.info())
		size_in_mb = int(d.get("Content-Length")) / 1024 / 1024
		print(('{:.2f}' + " MB").format(size_in_mb))

	except BaseException as e:
		print("Error:")
		print(url)
		print(e)
		return

	data = response.read()

	file = open(path, 'wb')
	file.write(data)
	file.close()

discs = input('How many discs? ')
discs = int(discs)
track_counts = []

for i in range(discs):
	inp = input('How many tracks on disk ' + str(i+1) + '? ')
	track_counts.append(int(inp))

url = input('URL of d1t01: ')
folder = input('Folder: ')
os.makedirs(folder,exist_ok=True)

endofurl = url.rsplit('/', 1)[-1]
startofurl = url.rsplit('/', 1)[0]

urls = []
for i in range(discs):
	current = endofurl
	veryend = current[:8]
	

	if('t' in veryend):
		current = current[:-8] # #t##.mp3
	else:
		current = current[:-7] # #t##.mp3

	current = current + str(i + 1)

	if('t' in veryend):
		current += 't01.mp3'
	else:
		current += '01.mp3'

	for j in range(track_counts[i]):
		copy = current
		# chop .mp3
		copy = copy[:-4]

		copy = copy[:-2]

		tracknum = j + 1
		if(tracknum < 10):
			tracknum = '0' + str(tracknum)
		else:
			tracknum = str(tracknum)

		url = startofurl + '/' + copy + tracknum + '.mp3'

		urls.append(url)

for url in urls:
	get_and_save(url, folder)