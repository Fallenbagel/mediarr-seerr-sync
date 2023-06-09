from flask import Flask, request, jsonify
from waitress import serve
import requests
import config
from urllib.parse import quote
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/webhook", methods=["POST"])
def webhook():
    # Get JSON payload from request
    json_data = request.get_json()
    title = json_data.get("title")
    tvdb_id = json_data.get("tvdb_id")
    tmdb_id = json_data.get("tmdb_id")
    imdb_id = json_data.get("imdb_id")
    #print(title)
    logging.info(f"'{title}' deleted from *arr...")
    main(title, tvdb_id, tmdb_id, imdb_id)
    return jsonify(success=True)

def api(method: str, endpoint: str, json: dict = None) -> requests.Response:
    url = config.URL.rstrip("/") + endpoint
    auth_data = {"x-api-key": config.KEY}

    response = requests.api.request(method, url, headers=auth_data, json=json)
    #print(response)
    return response

def main(title, tvdb_id, tmdb_id, imdb_id):
    logging.info(f"Searching '{title}' on seerr...")
    search = api("GET", f"/search?query={quote(title)}").json()
    search = [x["mediaInfo"] for x in search["results"] if "mediaInfo" in x]
    
    for item in search:
     if item is not None and any(id_value is not None for id_value in [item["tvdbId"], item["tmdbId"], item["imdbId"]]):
        env_ids = [tvdb_id, tmdb_id, imdb_id]
        seerr_ids = [item["tvdbId"], item["tmdbId"], item["imdbId"]]
        #print(env_ids)
        #print(seerr_ids)
        #print(item['id'])
        if any((x in seerr_ids and x is not None) for x in env_ids):
            if config.CLEAR_DATA:
                logging.info("Deleting media...")
                response = api("DELETE", f"/media/{item['id']}")  
                if response.status_code == 204:
                    logging.info(f"'{title}' deleted from seerr")
            else:
                logging.info("Posting issue...")
                issue_data = {"issueType": 4, "message": "Removed from library", "mediaId": item["id"]}
                response = api("POST", "/issue", json=issue_data)
                if response.status_code == 204:
                    logging.info(f"Posted an issue for '{title}' removal")

    #print(search)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0')