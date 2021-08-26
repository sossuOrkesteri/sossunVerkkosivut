import json, time, requests, re, os

def read_data_from_file(filename):
    with open(filename, "r") as file:
        return json.loads(file.read())

def write_data_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(json.dumps(data, indent=4))

secrets = {
    "user_id": os.getenv("USER_ID"),
    "access_token": os.getenv("ACCESS_TOKEN")
}
if "last_refresh" in os.environ:
    secrets["last_refresh"] = os.gerenv("LAST_REFRESH")
else:
    secrets["last_refresh"] = 0

def call(url, payload):
    """ Calls the instagram Basic Display API with the given url and payload.
    Returns the response body as a dict.
    Raises HTTPError if the HTTP response code is 4XX or 5XX. """
    # append access token to payload
    payload |= {"access_token": secrets["access_token"]}
    response = requests.get("https://graph.instagram.com" + url, params=payload, timeout=1)
    response.raise_for_status()
    return response.json()

def refresh_instagram_access_token():
    """ Refreshes the long-lived access token of the instagram account. The access token
    will expire in 60 days if not refreshed. A refresh is possible when at least 24 hours
    have passed since the previous one. """
    response_body = call("/refresh_access_token", {"grant_type": "ig_refresh_token"})
    expiration_date = time.time() + response_body["expires_in"]
    expiration_date = time.strftime("%Y.%m.%d %H:%M", time.gmtime(expiration_date))
    secrets["last_refresh"] = time.time()
    print(f"Instagram access token refreshed. Expires on {expiration_date}")
    return secrets

def format_media(media):
    """ Writes the media returned by the IG API in the desired format. """
    for entry in media:
        # date format
        timestamp = time.strptime(entry["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        entry["timestamp"] = time.strftime("%d.%m.%Y", timestamp)

        # remove hashtags from the ends of captions
        entry["caption"] = re.sub("(\s?#\S+)*$", "", entry["caption"])
    return media

def fetch_instagram_media():
    """ Fetches the most recent media of the instagram user. """
    print("Fetching instagram media.")
    fields = ",".join([
        "caption", "media_type", "media_url", "permalink",
        "thumbnail_url", "timestamp", "children"
    ])
    response_body = call("/{:s}/media".format(secrets["user_id"]), {"fields": fields})
    return format_media(response_body["data"])

if __name__ == "__main__":
    secrets = refresh_instagram_access_token()
    os.environ["LAST_REFRESH"] = str(secrets["last_refresh"])
    media = fetch_instagram_media()
    write_data_to_file("instagram_media.json", media)
