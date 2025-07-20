import requests
import streamlit as st
import isodate
import math

api_key = st.secrets['api_key']

class Data:
    def __init__(self, search_query=None):
        self.search_query = "+".join(search_query.split()) if search_query else ""
        self.unsorted_data = []
        self.sorted_result = []

    def fetch_data(self, maxResults=50, target_count = 50):
        # Search API

        search_url = "https://www.googleapis.com/youtube/v3/search"
        next_page_token = None
        searched_count = 0
        while (len(self.unsorted_data) < target_count):
            searched_count += 1
            search_params = {
                "key": api_key,
                "q": self.search_query,
                "part": "snippet",
                "type": "video",
                "maxResults": maxResults,
                "relevanceLanguage": "en",
                "pageToken" : next_page_token
            }

            search_response = requests.get(search_url, params=search_params)
            search_data = search_response.json().get("items", [])
            next_page_token = search_response.json().get("nextPageToken")

            video_ids = [item["id"]["videoId"] for item in search_data if "videoId" in item["id"]]

            # Stats API (batch call)
            video_url = "https://www.googleapis.com/youtube/v3/videos"
            video_params = {
                "key": api_key,
                "id": ",".join(video_ids),
                "part": "snippet,statistics,contentDetails",
            }

            video_response = requests.get(video_url, params=video_params)
            video_items = video_response.json().get("items", [])

            for video in video_items:
                
                snippet = video.get("snippet", {})
                stats = video.get("statistics", {})
                content = video.get("contentDetails",{})
            
                # getting duration of video
                duration = isodate.parse_duration(content['duration'])
                

                if int(duration.total_seconds()) > 60 :
                    video_data = {
                        "videoId": video.get("id"),
                        "title": snippet.get("title"),
                        "channelTitle": snippet.get("channelTitle"),
                        "description": snippet.get("description"),
                        "thumbnail_image": snippet.get("thumbnails", {}).get("high", {}).get("url"), # only get the high resolution  if available
                        "likes": stats.get("likeCount", 0),
                        "views": stats.get("viewCount", 0),
                        "comments": stats.get("commentCount", 0),
                        "tags" : snippet.get("tags"), # this is a list
                        "duration" : duration.total_seconds() # duration of video in seconds
                    }

                    self.unsorted_data.append(video_data)

                    if len(self.unsorted_data) >= target_count:
                        break
            if not next_page_token:
                break
        return searched_count
                

    def sort_data(self):
        #scoring each video

        for video in self.unsorted_data:
            view_score = math.log10(int(video["views"]) + 1)
            engagement_score = (int(video["likes"])+ int(video["comments"])) / (int(video["views"]) + 500) # 500 as a bias so that small sample win is reduced
            video["score"] = view_score * engagement_score * 100

        self.sorted_result = sorted(
            self.unsorted_data,
            key = lambda x : x["score"],
            reverse = True
        )
        return self.sorted_result


if __name__ == "__main__":
    data = Data("python")
    print(data.fetch_data())
    # print(data.sort_data())
