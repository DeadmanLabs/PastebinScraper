from bs4 import BeautifulSoup
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
}

count = 1
file = open(str(input("Please enter output file name: ")), 'a')
query = str(input("Please enter pastebin keyword: "))
verbose = bool(int(input("Would you like verbose output (0/1): ")))
address = "http://www.bing.com/search?q=site:pastebin.com+" + query
try:
    while True:
        print("Requesting " + address)
        response = requests.get(address, headers=headers)
        if verbose:
            print("[v] - response.status_code == " + str(response.status_code))
        if response.status_code == 200:
            print("Response Received! Reading Pages...")
            soup = BeautifulSoup(response.content, "html.parser")
            pages = soup.findAll('cite')
            print("Found " + str(len(pages)) + " sites!")
            for i in range(len(pages)):
                pages[i] = str(pages[i])
            print("Time To Start Lookin at pages")
            for i in range(len(pages)):
                if "pastebin.com" in pages[i]:
                    pages[i] = pages[i].replace('<cite>', '')
                    pages[i] = pages[i].replace('</cite>', '')
                    pages[i] = pages[i].replace('</strong>', '')
                    pages[i] = pages[i].replace('<strong>', '')
                    pages[i] = pages[i].replace('//', '//www.')
                    pages[i] = pages[i].replace('.com/', '.com/raw/')
                    print("Requesting " + pages[i] + "...")
                    data = requests.get(pages[i])
                    if data.status_code == 200:
                        print("Reading " + pages[i] + "...")
                        if verbose:
                            print("[v] - " + data.content)
                        results = re.search('^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', str(data.content))
                        if results != None:
                            print("Bitcoin address found at " + pages[i])
                            file.write(pages[i] + "\n")
                        else:
                            print("No address found")
                    else:
                        print("Error requesting page: " + str(data.status_code))
                else:
                    print("Non pastebin site detected: " + pages[i])
            count += 1
            next_pages = soup.findAll("a", class_="b_widePag sb_bp")
            print(str(next_pages))
            for next in next_pages:
                if next["aria-label"] == "Page " + str(count):
                    print("Proceeding to Page " + str(count))
                    address = "http://www.bing.com" + next["href"]
            
except KeyboardInterrupt:
    print("Closing...")
file.close()