
import streamlit as st

from data_fetcher import Data # from data_fetcher.py

st.set_page_config(page_title="YouTube Video Finder", layout = "wide")

st.title("Youtube Video Finder")

search_query = st.text_input("Enter search query")


min_duration_sec = st.slider(
    min_value=1, 
    max_value=30, 
    value=2, 
    step=2,
    label = "Minimum Duration in Minutes"
) * 60

if st.button("Search"):
    with st.spinner("Fetching videos... Standby."):
        data_fetcher = Data(search_query)
        search_count = data_fetcher.fetch_data(target_count=50)


        sorted_videos = data_fetcher.sort_data()
        filtered = [
            video for video in data_fetcher.sorted_result
            if video["duration"] >= min_duration_sec/60
        ]
        if not filtered:
            st.warning("No videos found..")
        else:
            st.success(f"Found {len(filtered)} videos (searched {search_count} pages)")
            for i, video in enumerate(sorted_videos[:10]):
                cols = st.columns([1, 2])

                with cols[0]:
                    video_url = f"https://www.youtube.com/watch?v={video['videoId']}"
                    st.markdown(
                        f'<a href="{video_url}" target="_blank">'
                        f'<img src="{video["thumbnail_image"]}" /></a>',
                        unsafe_allow_html=True
                    )

                with cols[1]:
                    st.subheader(f"{i+1}. {video['title']}")
                    st.write(f"Channel: {video['channelTitle']}")
                    st.write(f"Duration: {int(video['duration'] // 60)} min {int(video['duration']%60)} sec")
                    st.write(f"👁️ {video['views']} &nbsp;&nbsp;  👍{video['likes']} &nbsp;&nbsp; 💬 {video['comments']}")

                st.markdown("-------------------------------")
