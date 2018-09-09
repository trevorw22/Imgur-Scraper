#! python3
# imgurSearch.py - Imgur Image Downloader
# This is an imgur image scraper I made using requests and beautiful soup 4.
# This was my first real image scraping program, and still needs some work.
# Usage: python imgurSearch.py searchWord
# Note: You can use "search words" in quotes if you want to pull images with multiple tags.

import requests, os, sys, bs4

url = 'http://imgur.com/search?q=' + ' '.join(sys.argv[1:])
print('Pinging Imgur...')
os.makedirs('imgur', exist_ok=True)
while not url.endswith('#'):
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	# imgElem = soup.find_all('img')
	for images in soup.find_all('img'):
		# imgElem = soup.select('img')
		# imgElems = soup.findall('a', 'image-list-link')

		try:
			imgUrl = 'http:' + images.get('src')
			# Download the image
			print('Downloading image %s from imgur...' % (imgUrl))
			res = requests.get(imgUrl)
			res.raise_for_status()

		except requests.exceptions.MissingSchema:
			print('Error downloading this image...')
			continue
		imageFile = open(os.path.join('imgur', os.path.basename(imgUrl)), 'wb')

		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()

# TODO Click image and save it from the results, then go back

print('Done.')
