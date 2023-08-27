import random 
import requests
import time
from threading import Timer 

proxies = open("bypass\proxy_list.txt", "r").read().strip().split("\n")

unchecked = set(proxies[0:25])
working = set() 
not_working = set() 

def reset_proxy(proxy): 
	unchecked.add(proxy) 
	working.discard(proxy) 
	not_working.discard(proxy) 
 
def set_working(proxy): 
	unchecked.discard(proxy) 
	working.add(proxy) 
	not_working.discard(proxy) 
 
 
def set_not_working(proxy): 
	unchecked.discard(proxy) 
	working.discard(proxy) 
	not_working.add(proxy) 
 
	# move to unchecked after a certain time (20s in the example) 
	Timer(20.0, reset_proxy, [proxy]).start()
 
def get_random_proxy(): 
	# create a tuple from unchecked and working sets 
	with open("proxies.txt", "r") as working_proxy_n:
		available_proxies = tuple(working_proxy_n) 
	if not available_proxies: 
		raise Exception("no proxies available") 
	return random.choice(available_proxies)

VALID_STATUSES = [200, 301, 302, 307, 404] 

session = requests.Session() 
		
def get(url, proxy=None):
    if not proxy:
        proxy = get_random_proxy()

    try:
        response = session.get(url, proxies={'http': f"http://{proxy}"}, timeout=30)
        if response.status_code in VALID_STATUSES:
            set_working(proxy)
        else:
            set_not_working(proxy)

        return response
    except (requests.exceptions.RequestException, Exception) as e:
        set_not_working(proxy)
        print(f"Error while making request with proxy {proxy}: {e}")
        return None

 
def check_proxies(): 
	for proxy in list(unchecked): 
		get("http://ident.me/", proxy) 
		time.sleep(1)
		
check_proxies()

 
print("unchecked ->", unchecked) 
print("working ->", working) 
print("not_working ->", not_working) 

with open("proxies.txt", "w") as working_proxy:
	working_proxy.write(str(working))

print("Proxy File Saved")

print(get_random_proxy)