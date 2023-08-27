import requests
# import schedule
# import time

def job():
    url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
    response = requests.get(url)

    if response.status_code == 200:
        ip_addresses = response.text.split()
        if ip_addresses is None:
            print("Error: Failed to fetch proxies from the API.")
        else:
            with open("proxy_list.txt", "w") as proxy_list:
                for proxy in ip_addresses:
                    proxy_list.write("%s\n" % (proxy))
            print("Proxies Saved")
    else:
        return None
    
# schedule.every(60).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)