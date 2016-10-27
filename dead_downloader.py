import urllib.request
import sys
import os
import re

def get_and_save(url, folder):
	filename = url.rsplit('/', 1)[-1]
	path = folder + '/' + filename;

	print(url)

	try:
		response = urllib.request.urlopen(url)
		headers = response.info()
		d = dict(response.info())
		size_in_mb = int(d.get("Content-Length")) / 1024 / 1024
		print(('Downloading {:.2f}' + ' MB...').format(size_in_mb))

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
folder = input('Output folder: ')
os.makedirs(folder, exist_ok=True)

endofurl = url.rsplit('/', 1)[-1]
startofurl = url.rsplit('/', 1)[0]
disc_track_re = re.compile('d[0-9]t?[0-9][0-9]')

urls = []
for i in range(discs):
	current = endofurl
	#formats:
	# d1t01
	# d101
	# above with string after eg d1t01-ASDF.mp3
	match = disc_track_re.findall(current)
	# will fail if multiple matches
	match = match[0]
	# disc #
	replacement = match
	replacement = replacement[0] + str(i+1) + replacement[2:]

	for j in range(track_counts[i]):
		tracknum = j + 1
		if(tracknum < 10):
			tracknum = '0' + str(tracknum)
		else:
			tracknum = str(tracknum)

		replacement = replacement[:-2] + tracknum

		url = startofurl + '/' + current.replace(match, replacement)

		urls.append(url)

for url in urls:
	get_and_save(url, folder)
	#print(url)
