import gunicorn

bind = "0.0.0.0:5589"
workers = 1
timeout = 3600
threads = 1
reload = False
gunicorn.SERVER = 'HiddenWebServer'

