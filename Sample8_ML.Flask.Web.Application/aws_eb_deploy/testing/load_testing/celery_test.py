import redis

# List of Redis URLs to test
redis_urls = [
    'redis://andrew:01237459wDX@redis:6379/0',
    'redis://andrew:01237459wDX@redis_container:6379/0',
    'redis://andrew:01237459wDX@redis:6379/1',
    'redis://andrew:01237459wDX@redis_container:6379/1',
    'redis://andrew:01237459wDX@redis:6379/2',
    'redis://andrew:01237459wDX@redis_container:6379/2',
    'redis://redis:6379/0',
    'redis://redis_container:6379/0',
    'redis://redis:6379/1',
    'redis://redis_container:6379/1',
    'redis://redis:6379/2',
    'redis://redis_container:6379/2'
]

# Test each Redis URL
for url in redis_urls:
    try:
        r = redis.Redis.from_url(url)
        r.ping()
        print(f"Connected to Redis at {url}")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis at {url}: {e}")
