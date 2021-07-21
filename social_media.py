import json, time, requests

def read_data_from_file(filename):
    with open(filename, "r") as file:
        return json.loads(file.read())

def write_data_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(json.dumps(data, indent=4))

try:
    secrets = read_data_from_file("secrets.json")
except FileNotFoundError:
    secrets = {"user_id": "", "access_token": "", "last_refresh": 0}
    write_data_to_file("secrets.json", secrets)

def call(url, payload):
    """ Calls the instagram Basic Display API with the given url and payload.
    Returns the response body as a dict.
    Raises HTTPError if the HTTP response code is 4XX or 5XX. """
    # append access token to payload
    payload |= {"access_token": secrets["access_token"]}
    response = requests.get("https://graph.instagram.com" + url, params=payload)
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
    write_data_to_file("secrets.json", secrets)

def fetch_instagram_media():
    """ Fetches the most recent media of the instagram user. """
    print("Fetching instagram media.")
    fields = ",".join([
        "caption", "media_type", "media_url", "permalink",
        "thumbnail_url", "timestamp", "children"
    ])
    response_body = call("/{:s}/media".format(secrets["user_id"]), {"fields": fields})
    media = response_body["data"]
    write_data_to_file("instagram_media.json", media)

if __name__ == "__main__":
    refresh_instagram_access_token()
    fetch_instagram_media()
