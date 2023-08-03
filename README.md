# Sossu flask
This is the sossu's main page.

## Running
To run this on this server, one should just start the systemd service sossu-flask.service with
the command 
```bash
systemctl start sossu-flask.service
```

There exists a symlink from `sossunVerkkosivut/sossu-flask.service -> /etc/systemd/system/sossu-flask.service`.
The systemd service file waits for network connectivity before starting and should be enabled by default to run
after system rebooting or on failure.

If systemd service is not needed the app can be run by 
```bash
python wsgi.py
```


## Virtual environment
If one needs to update the `pip` packages or something else to do with such things, there exists a virtual env
at `.venv`. If that does not exist, create it with `python -m venv .venv`

After that you need to activate it with (in linux at least)
```bash
source .venv/bin/activate
```

Then you can install the required packages with
```bash
pip install -r requirements.txt
```
