# For configuration details go to:
# http://docs.gunicorn.org/en/stable/configure.html
# https://docs.gunicorn.org/en/stable/settings.html

# Server Socket
backlog = 2048  # default
bind = "0.0.0.0:8000"

# Worker Processes
graceful_timeout = 65
keepalive = 65  # default
max_requests = 0  # default
timeout = 65
worker_class = "sync"
worker_connections = 1000  # default
workers = 1
threads = 8

# Security
limit_request_fields = 100  # default
limit_request_field_size = 8190  # default
limit_request_line = 4094  # default


# Server Mechanics
chdir = "usr/src/app"
daemon = False  # default
group = None  # default
pidfile = "usr/src/app/gunicorn.pid"
umask = 0  # default
user = None  # default
worker_tmp_dir = "/dev/shm"   # http://docs.gunicorn.org/en/stable/faq.html#blocking-os-fchmod

# Debugging
reload = True

# Logging
accesslog = "-"
errorlog = "-"  # default
loglevel = "debug"
