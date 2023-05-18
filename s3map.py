import requests
import re
import time
import sys, getopt

fileRegions = open('regions', 'r')
regions = fileRegions.readlines()

argv = sys.argv[1:]

bucketName = "Null"
verbose = False
regionAlt = "All"
path = ""

chooseRegions = []
foundBuckets = []

def Help():
    print("[?] Help")
    sys.exit()

opts, args = getopt.getopt(argv,"hn:r:vp:",["bucketName=","regions=","path="])
for opt, arg in opts:
    if opt == '-h':
        Help()
    elif opt in ("-n", "--buckerName"):
        bucketName = arg
    elif opt in ("-r", "--regions"):
        regionAlt = arg
    elif opt in ("-v", "--verbose"):
        verbose = True
    elif opt in ("-p", "--path"):
        path = arg 

def infoValidator():
    if bucketName == "Null":
        print("[X] You need to specify a bucket name")
        Help()    
    
    Passed = False
    if regionAlt != "All":
        regionsValues = regionAlt.split(",")
        for value in regionsValues:
            for available in regions:
                if(value == available.replace("\n","")):
                    Passed = True
            if Passed == False:
                print("[X] The specified region does not exist")
                Help()
            else:
                Passed = False


def Banner():
    print("[*] s3map Started ")
    print("[*] Searching at [" + bucketName + "]")
    print("[*] Regions: " + regionAlt)
    print("[*] Verbose: " + str(verbose))
    print("[*] Path: /" + path)
    print("[...]")
    print("")
infoValidator()
Banner()


if(regionAlt != "All"):
    chooseRegions = regionAlt.split(",")
else:
    chooseRegions = regions

try:

    for region in chooseRegions:
        regionName = region.replace('\n','')

        currentUrl = "https://{}.s3.{}.amazonaws.com".format(bucketName,regionName)
        if(path != ""):
            currentUrl = currentUrl+"/"+path

        code = requests.head(currentUrl)
        codeNum = re.findall("\[(.*?)\]",str(code))[0]

        if verbose:
            print("[>] " + currentUrl + " - "+codeNum)

        if codeNum == "403":
            foundBuckets.append(currentUrl+" - "+codeNum+" Forbidden")
        elif codeNum == "200":
            foundBuckets.append(currentUrl+" - "+codeNum+" Ok")
        time.sleep(0.5)

    if(len(foundBuckets) > 0):
        print("")
        print("[!] Found:")
        for index in foundBuckets:
            print("[-->] "+index)
    else:
        print("")
        print("[ :( ] Nothing Found")
except:
    sys.exit()
