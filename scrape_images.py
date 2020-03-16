import urllib.request
import threading
import time


class ScrapeTwoInchBrush(object):

    base_url = "https://www.twoinchbrush.com/images/painting"
    file_path = "raw_data/"
    pool_size = 32
    amount_of_images = 0
    total_time = 0

    def saveImage(self, url, file_num):
        file_path = self.file_path + "{}.png".format(str(file_num).zfill(3))
        urllib.request.urlretrieve(url, file_path)
        self.amount_of_images += 1

    def getImages(self, image_num):
        url = self.base_url + "{}.png".format(image_num)
        try:
            self.saveImage(url, image_num)
        except urllib.error.HTTPError:
            print("Failed to get {}".format(image_num))

    def scrape(self, search_range=(0, 500)):
        threads = [threading.Thread(target=self.getImages, args=(
            image_num,)) for image_num in range(*search_range)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def pool(self, search_range):
        old = search_range[0]
        start = time.time()
        for search_range in range(0, search_range[1], self.pool_size):
            self.scrape((old, search_range + self.pool_size))
            old = search_range + self.pool_size
        self.total_time += time.time() - start


scraper = ScrapeTwoInchBrush()
scraper.pool((0, 412))
print(scraper.total_time)
print(scraper.amount_of_images)
