# -*- coding: utf-8 -*-

import certstream
import os
import yaml
import time
import requests
import json


# certstream websocket URL 
url='wss://certstream.calidog.io/'

# domain list to monitor
domains_yaml = os.path.dirname(os.path.realpath(__file__))+'/domains.yaml'

# output file 
found_domains_path = os.path.dirname(os.path.realpath(__file__))+'/output/found-domains.log'

# function to send slack notifications
def slack_notifier(unique_subdomains):
    webhook_url = webhook['SLACK_WEBHOOK']

    # data to send in slack notifications
    slack_data = {
        'username' : 'certeagle-bot' , 
        'channel': '#subdomain-monitor' , 
        'text': 
            "🔴 CertEagle Alert : \n\n" + "✔️ Domain matched : " + str(len(unique_subdomains)) + "\n\n" +'\n'.join(unique_subdomains) 
        }
    
    #print(slack_data)
    
    response = requests.post(
	    webhook_url, data=json.dumps(slack_data),
	    headers={'Content-Type': 'application/json'}
	)

    return 



# function to extract and parse subdomains/domains related to our specified domains
def parse_results(all_domains_found):
    seen_domains = []
    
    for subdomain in all_domains_found:
        if any(word in subdomain for word in domain_list['domains']):
            # removing wildcards
            if subdomain.startswith("*"):
                seen_domains.append(subdomain[2:])
            else:
                seen_domains.append(subdomain)

    # we have a list of found domains now (which might be containing some duplicate entries)
    # Lets get rid of duplicate entries

    if len(seen_domains) > 1:
        unique_subdomains = list(set(seen_domains))

         # checking if domain already exists in already seen file
        
       
        for t in unique_subdomains:
            print("\u001b[32m[MATCH]\u001b[0m : " + t )
            with open(found_domains_path, 'a') as f:
                    f.write(time.strftime("%Y-%m-%d") + " {}\n".format(t))


        # checking if a hook url is supplied , if yes then sending notifications
        if webhook['SLACK_WEBHOOK'].startswith("https://hooks.slack.com/"):
            for t in unique_subdomains:
                try:
                    #open and match 
                    with open('already-seen.log' , 'r') as f:
                        already_seen = f.read().splitlines()
                        if any(word in t for word in already_seen):
                            pass
                        else:
                            #send notifications
                            slack_notifier(unique_subdomains)
                            with open('already-seen.log' , 'a') as writer:
                                writer.write('\n'.join(unique_subdomains))
                                writer.write('\n')

                except Exception as e:
                    pass    

    return 

    
# callback function
def print_callback(message, context):

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        # checking if domain list is empty
        if len(all_domains) == 0:
            pass
        else:
           parse_results(all_domains)
 

if __name__ == "__main__":

    # reading the domains file
    with open(domains_yaml, 'r') as f:
        try:
            domain_list  = yaml.safe_load(f)
        except yaml.YAMLError as err:
            print(err)
    
    # reading the config file
    with open('config.yaml', 'r') as f:
        try:
            webhook  = yaml.safe_load(f)
            # access var : webhook['SLACK_WEBHOOK']
        except yaml.YAMLError as err:
            print(err)

    banner = """\u001b[32;1m
    _______ _______  ______ _______ _______ _______  ______        _______
    |       |______ |_____/    |    |______ |_____| |  ____ |      |______
    |_____  |______ |    \_    |    |______ |     | |_____| |_____ |______
                                                                        
                             - coded with \u001b[31;1m<3\u001b[0m \u001b[32;1mby Devansh Batham\u001b[33;1m(@0xAsm0d3us)

    \u001b[0m"""
    if os.name == 'nt':
        os.system('cls')
    print(banner)

    # displaying basic information
    print("\u001b[32m[INFO]\u001b[0m No of domains/Keywords to monitor  " + str(len(domain_list['domains'])))
    if webhook['SLACK_WEBHOOK'].startswith("https://"):
        print("\u001b[32m[INFO]\u001b[0m Slack Notifications Status - \u001b[32;1mON\u001b[0m")
    else:
        print("\u001b[32m[INFO]\u001b[0m Slack Notifications Status - \u001b[31;1mOFF\u001b[0m")



    certstream.listen_for_events(print_callback, url=url)