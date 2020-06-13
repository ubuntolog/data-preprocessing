import requests, re, json, time, logging, os, sys
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
MAX_RESULT = 1000

def search(keywords, class_name, out):
    os.mkdir(out + class_name)
    url = 'https://duckduckgo.com/'
    params = {
    	'q': keywords
    }

    logger.debug("Getting a Token")

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I)

    if not searchObj:
        logger.error("Token Parsing Failed !")
        return -1

    logger.debug("Obtained Token")

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js"

    logger.debug("Hitting Url : %s", requestUrl)
    counter = 0
    while True:
        while True:
            try:               
                res = requests.get(requestUrl, headers=headers, params=params, timeout=5)
                data = json.loads(res.text)
                
                break
            except ValueError as e:
                logger.error(e)
                logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl)
                time.sleep(5)
                continue

        logger.debug("Hitting Url Success : %s", requestUrl)
        # print(len(data["results"]))
        # # date_time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        # print("date and time:",date_time)	
        printJson(data["results"], class_name, counter, out)
        counter = counter + len(data["results"])
       

        if "next" not in data:
            logger.debug("No Next Page - Exiting")
            return

        requestUrl = url + data["next"]

def printJson(objs, subfolder, counter, out):
    for obj in objs:
        counter = counter + 1
        print ("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        print ("Thumbnail {0}".format(obj["thumbnail"]))
        print ("Url {0}".format(obj["url"]))
        print ("Title {0}".format(obj["title"].encode('utf-8')))
        print ("Image {0}".format(obj["image"]))
        print (counter)
        print ("__________")

        file_name = obj["image"].split(".")
        if len(file_name)>0:     
            extension = file_name[-1]    
            extra_chars = file_name[-1].split("?", 1)  
            if (len(extra_chars)>0):
                extension = file_name[-1].split("?", 1)[0]

            saveImage(obj, str(counter), extension, subfolder, out)

        if (int(counter)>MAX_RESULT):
            sys.exit("Image number limit has been reached")




def saveImage(obj, out_name, out_extension, subfolder, out):    
    img_link = obj['image']

    try:
        img_data = requests.get(img_link, timeout=5).content
        
        filename = out + subfolder + "/" + out_name + "." + out_extension
        try:
            with open(filename, 'wb+') as f:
                f.write(img_data)
        except:
            print("Cannot save an image")

        print("File " + filename + " successfully downloaded")
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    if len(sys.argv) < 2:
        print ("Arg #1: output folder")
        sys.exit("Looks like you did not specify the destination folder")        

    data_out = sys.argv[1]
  

    food = [ 
        ["olive oil", "olive_oil"],
        ["fried meat", "fried meat"]
    ]

    for f in food:
        print(f[0], f[1])    
        search(f[0], f[1], data_out)