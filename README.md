# Python Ratelimit
An operations rate limiter for python.

Supporting only Python 3.6 and newer.

## Usage
Ideally used for rate limiting Client API requests.

## Examples
### Simple Example
```python
import ratelimit

simulated_results = []
# create limiter to allow 20 triggers within 2 minutes
ratelimiter = ratelimit.RateLimit(20, 120)

for idx in range(40):
    ratelimiter.trigger()
    simulated_results.append("%4d - %s" % (idx, time.time(),))

```

### Advanced Example
Creating an API Client class that can respect an API services requests limit.
```python
import ratelimit

class ApiClient:
	def __init__(self):
		self.__ratelimit = ratelimit.RateLimit(20, 120)
		self.__http_client = requests.Session()
	
	def get(self, endpoint):
		self.__ratelimit.trigger()
		self.__http_client.get(endpoint)
```
## To Do
* Enable library to be installed via pip
