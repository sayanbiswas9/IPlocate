#!/bin/python3
# *-* coding: utf-8 -*-

import os
import requests
import socket
import sys

# Version
version = "3.0"
# Colors foridentificationn of output

def supports_color():
    supported_platform = sys.platform != 'win32' or 'ANSICON' in os.environ or 'WT_SESSION' in os.environ
    is_a_tty = sys.stdout.isatty()
    return supported_platform and is_a_tty

class color:
    if supports_color():
        ERROR = '\033[31m'
        OK = '\033[32m'
        INFO = '\033[33m'
        ONION = '\033[35m'
        WHITE = '\033[94m'
        BO = '\033[1m'
        DIM = '\033[2m'
        IT = '\033[3m'
        UN = '\033[4m'
        RESET = '\033[0m'
    else:
        ERROR = ''
        OK = ''
        INFO = ''
        WHITE = ''
        ONION = ''
        BO = ''
        DIM = ''
        IT = ''
        UN = ''
        RESET = ''

# IPLocate Guide
help_message = """
    IPLocate v1.0.1
    Usage: iplocate [OPTIONS] [ARGUMENTS]

    Options:
    -h, help         Show this help message and exit
    localhost        Get the current user's public IP
    [domain/IP]      Get information about the provided domain or IP
    -f, --fields     Specify the fields to retrieve (comma-separated)

    Example:
    iplocate example.com -f country,city,isp
    
    Fields:
    continent,continentCode,country,countryCode,regionName,region,city,zip,offset,currency,lat,lon,timezone,isp,org,as,asname,mobile,proxy,hosting,query
    """

# Print statement dictionary
def states(query, data):
    statements = {
        "continent": f"  Continent: {data.get('continent', 'N/A')}",
        "continentCode": f"  Continent Code: {data.get('continentCode', 'N/A')}",
        "country": f"  Country: {data.get('country', 'N/A')}",
        "countryCode": f"  Country Code: {data.get('countryCode', 'N/A')}",
        "regionName": f"  Region/State: {data.get('regionName', 'N/A')}",
        "region": f"  Region Code: {data.get('region', 'N/A')}",
        "city": f"  City: {data.get('city', 'N/A')}",
        "district": f"  District: {data.get('district', 'N/A')}",
        "zip": f"  ZIP/PIN: {data.get('zip', 'N/A')}",
        "lat": f"  Latitude: {data.get('lat', 'N/A')}",
        "lon": f"  Longitude: {data.get('lon', 'N/A')}",
        "timezone": f"  Timezone: {data.get('timezone', 'N/A')}",
        "offset": f"  Offset: {data.get('offset', 'N/A')}",
        "currency": f"  Local Currency: {data.get('currency', 'N/A')}",
        "isp": f"  ISP: {data.get('isp', 'N/A')}",
        "org": f"  Organization: {data.get('org', 'N/A')}",
        "as": f"  AS: {data.get('as', 'N/A')}",
        "asname": f"  ASNAME: {data.get('asname', 'N/A')}",
        "mobile": f"  Mobile: {getYesNo(data.get('mobile', False))}",
        "proxy": f"  Proxy: {getYesNo(data.get('proxy', False))}",
        "hosting": f"  Hosting: {getYesNo(data.get('hosting', False))}",
        "query": f"  Query: {data.get('query', 'N/A')}"
    }
    return statements.get(query, f"  {query}: Not Available")

# Function to convert boolean to Yes/No
def getYesNo(query):
    return "Yes" if query else "No"

# Functions for the tool
def ownIP():
    API = "http://ip-api.com/json/?fields=query"
    response = requests.get(API)
    response.raise_for_status()
    try:
        response_in_json = response.json()
        IP = response_in_json["query"]
        return IP
    except requests.exceptions.RequestException:
        return None

# Checking if internet is connected
def check_internet():
    # Trying to connect to a well-known host
    try:
     # Attempt to make a request to a reliable website
        response = requests.get("https://www.google.com", timeout=5)
        # If the response status code is 200, the connection is successful
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False

# Getting IP addresses of the argumented hosts using their domain names
def convertDomain(domain):
    if not check_internet():
      print(color.ERROR + " [!] Couldn't connect to API! Try checking the network settings of your device." + color.RESET)
      sys.exit(1)
    if domain.split(".")[-1:] == "onion":
      print(color.ONION + " [i] This tool cannot locate hosts in the Dark Web." + color.RESET)
      sys.exit(1)
    # Getting host address from domain name
    try:
        IP = socket.gethostbyname(domain)
        return IP
    except:
        print(color.ERROR + " [!] Invalid domain name or argument!" + color.RESET)
        return None

# Main object of the program
def getInfo(IP, FIELDS):
    # If invalid domain or address is found, then IP contains no value. So exit.
    if not IP:
        sys.exit(0)
        
    fields = "continent,continentCode,country,countryCode,regionName,region,city,zip,offset,currency,lat,lon,timezone,isp,org,as,asname,mobile,proxy,hosting,query"
    if FIELDS:
        user_valid = [f for f in FIELDS if f in fields]
        not_valid = [f for f in FIELDS if f not in fields]
        API = "http://ip-api.com/json/" + IP + "?fields=status,message," + ",".join(user_valid)
    else:
        API = "http://ip-api.com/json/" + IP + "?fields=status,message," + fields

    try:
        response = requests.get(API)
        response.raise_for_status()
        data = response.json()

        try:
            hostname, _, _ = socket.gethostbyaddr(IP)
        except:
            hostname = None
    

        if data["status"] != "success":
            if data["message"] == "private range":
                print(color.ERROR + " [i] Private IP addresses aren't locatable. " + color.RESET)
                sys.exit(1)
            elif data["message"] == "invalid query":
                print(color.BO + " [!] " + color.ERROR + "Wrong IP address or invalid format." + color.RESET)
                sys.exit(1)
    
            else:
                print(color.ERROR + " [i] There's an unknown error reported by API for the provided IP address. Post your issue at " + color.UN + "https://github.com/sayanbiswas9/iplocate.git" + color.RESET)
                sys.exit(1)

        if FIELDS:
            for value in user_valid:
                print(states(value, data))
            if FIELDS and len(not_valid) != 0:
              print(color.ERROR + " [!] Wrong fields " + color.UN + ",".join(not_valid) + color.RESET + color.ERROR + " aren't shown!" + color.RESET)
            if "hostname" in FIELDS:
              print(color.INFO + " [i] Hostname with custom fields is currently unavailable. Try without fields to get that." + color.RESET)
            print("")
        else:
            location_group = fields.split(",")[0:9]
            coordinate_group = fields.split(",")[10:13]
            network_group = fields.split(",")[14:17]
            host_type_group = fields.split(",")[18:]

            print("")
            print(color.OK + color.BO + "[+] Location Information:" + color.RESET)
            for i in location_group:
              if i in ["continentCode", "countryCode", "region"]:
                continue
              elif i == "continent":
                print(f"{states(i, data)} ({data['continentCode']})")
              elif i == "country":
                print(f"{states(i, data)} ({data['countryCode']})")
              elif i == "regionName":
                print(f"{states(i, data)} ({data['countryCode']})")
            print(f"{states(i, data)}")

            print(color.OK + color.BO + "[+] Coordinates: " + color.RESET)
            for i in coordinate_group:
                print(states(i, data))
                
            print(color.OK + color.BO + "[+] Network Information: " + color.RESET)
            print(f"  Hostname: {hostname}")
            for i in network_group:
                print(states(i, data))

            print(color.OK + color.BO + "[+] Host Type: " + color.RESET)
            for i in host_type_group:
                print(states(i, data))
            print("")
            print(color.DIM + "*API provided by " + color.UN + "ip-api.com" + color.RESET)
            print("")

    except requests.exceptions.HTTPError:
        print(color.ERROR + " [!] Error occurred while sending request to API!" + color.RESET)
        sys.exit(1)

# Making the script work according to provided arguments
args = sys.argv

def main():
  if len(args) <= 1:
      print(help_message)
      sys.exit(0)
  
  if len(args) == 2:
      if args[1] in ("-h", "--help"):
          print(help_message)
          sys.exit(0)
        
      elif args[1] in ("-v", "--version"):
          print(color.INFO + f"[i] IPLocate here is on Version {version}." + color.RESET)

      elif args[1] == "localhost" or str(args[1]) == str(socket.gethostname()):
          localhost = ownIP()
          if localhost:
              getInfo(localhost, None)
          else:
              print(color.ERROR + " [!] There's an error while sending HTTP request to API" + color.RESET)
              sys.exit(1)

      else:
          l_list = [l.isalpha() for l in str(args[1])]
          if True in l_list:
              IP = convertDomain(str(args[1]))
          else:
              IP = args[1]
          getInfo(IP, None)

  if len(args) > 2:
      if args[2] == "-f" or args[2] == "--fields":
          if args[1] == "localhost" or args[1] == socket.gethostname():
              IP = ownIP()
          else:
              l_list = [l.isalpha() for l in args[1]]
              if True in l_list:
                  IP = convertDomain(str(args[1]))
              else:
                  IP = args[1]

          if args[3:]:
              getfields = args[3].split(',')
          else:
              getfields = None

          getInfo(IP, getfields)

      else:
          print(color.ERROR + " Unknown argument(s): " + ",".join(args[2:]) + color.RESET)
          sys.exit(1)
        

if __name__ == '__main__':
    main()
  
  
# EndOfScript