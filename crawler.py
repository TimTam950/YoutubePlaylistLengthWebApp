import requests
import datetime
import re
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, url):
        self.playlist_url = url

    @staticmethod
    def parse_length(request):
        soup = BeautifulSoup(request.content, 'html.parser')
        results = soup.find_all('div', {"class": "timestamp"})
        times = []
        for result in results:
            times.append(result.find_all(text=True))
        return times

    @staticmethod
    def process_times(times_list):
        single_times = []
        minutes = []
        seconds = []

        for time in times_list:
            single_times.append(time[0])

        for time in single_times:
            found = re.search('([0-9]+):([0-9]{2})', time)
            if found:
                minutes.append(int(found.group(1)))
                seconds.append(int(found.group(2)))

        total_seconds = sum(minutes) * 60 + sum(seconds)

        return total_seconds

    @staticmethod
    def calculate_length(total_seconds):
        val = str(datetime.timedelta(seconds=total_seconds))
        result = "Length of Playlist (H:M:S): {}".format(val)
        return result

    def run(self):
        try:
            playlist_request = requests.get(self.playlist_url)
            times = self.parse_length(playlist_request)
            total_seconds = self.process_times(times)
            playlist_length = self.calculate_length(total_seconds)
            return playlist_length
        except:
            return "error"
