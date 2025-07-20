# YouTube Video Filter

A simple YouTube video discovery tool that helps to find videos based on custom duration filters and engagement metrics.

## Features ✨

- **Search**: Search YouTube videos with custom queries
- **Duration Filter**: Set minimum video duration limits beyond three category range
- **Engagement-Bases Ranking**: Videos are ranked by custom scoring algorithm considering likes, comments, and views
- **Clean Interface**: Simple and straight-forward Streamlit web interface
- **Clickable Thumbnails**: Direct links to YouTube videos

## How it works 🛠️

1. Enter search query
2. Adjust duration filter if needed using sliders
3. Click "Search" to fetch videos
4. View list of results after ranking

The app used YouTube's Data API v3 to:
- Search for video matching query
- Fetch the detailed statistics of video
- Apply custom filter balancing popularity with engagement quality
    ```python
    view_score = log10(views + 1)
    engagement_score = (likes + comments) / (views + 500)
    final_score = view_score × engagement_score × 100
    ```

## Demo 🚀

## Local Setup and Installation ⚙️

### Prerequisities
- Python 3.7+
- YouTube Data API v3 key ([Get one here](https://developers.google.com/youtube/v3/getting-started
))

### Installation
1. Clone this Repository
```bash
git clone https://github.com/mSujal/YouTube-Filter.git
cd YouTube-Filter
```
2. Make Virtual Enviroment (Optional)
```bash
python -m venv .env
source .env/bin/activate
```
3. Install dependencies
```bash
pip install -r requirement.txt
```
4. Setup your Api key
- Create a .streamlit/secrets.toml file 
- Add your API key:
    ```toml
    api_key = "your-youtbe-api-key-here"
    ```

5. Run the app
```bash
streamlit run app.py
```
