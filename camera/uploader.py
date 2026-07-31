import os
from urllib import response
import requests

class Uploader:
    def __init__(self, server_url):
        self.server_url = server_url

    def upload(self, filename):
        print(f"Uploading {filename} to {self.server_url}")

        with open(filename, "rb") as video_file:
            response = requests.post(
                f"{self.server_url}/upload",
                files={
                    "video": (
                        os.path.basename(filename),
                        video_file,
                        "video/mp4"
                    )
                }
            )
        print(response.status_code)
        print(response.text)
        