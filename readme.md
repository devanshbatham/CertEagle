## CertEagle - Asset monitoring utility using real time CT log feeds
![certeagle](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/logo.PNG)

### Detailed Description about this can be found here :
Read Blog here : https://medium.com/@Asm0d3us/weaponizing-live-ct-logs-for-automated-monitoring-of-assets-39c6973177c7

### Introduction
In Bugbounties “**If you are not first , then you are last**” there is no such thing as silver or a bronze medal , Recon plays a very crucial part and if you can detect/Identify a newly added asset earlier than others then the chances of you Finding/Reporting a security flaw on that asset and getting rewarded for the same are higher than others.

Personally I am monitoring CT logs for domains/subdomains for quite a long time now and it gave me a lot of successful results , The inspiration behind this was “[Sublert : By yassineaboukir](https://github.com/yassineaboukir/sublert/)” which checks crt.sh for subdomains and can be executed periodically , However I am using somewhat different approach and instead of looking into crt.sh periodically, I am extracting domains from Live CT log feeds , So chances of me finding a new asset earlier is higher as compared to others.

### Workflow 
 -  Monitoring Real Time CT log feed and extracting the domain names from that feed
-   Matching the extracted subdomains/domains against the domains/Keywords to be matched
-   Sending a Slack notification if a domain name matches

#### Requirements :

-   A VPS (UNIX up and running)
-   Python 3x (Tested with Python 3.6.9)
-   Slack Workspace (optional)

### Setup 
I am assuming that you have already done with your setup of slack workspace .

Now Create a channel named “subdomain-monitor” and set up a incoming webhook

#### Enabling Slack Notifications :

Edit `config.yaml` file and paste your slack webhook URL there , It should look something like this
![config](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/config.png)

#### Keywords and domains to match :

You can specify keywords and domains to match in `domains.yaml` file , You can specify names

**For Matching subdomains :**

![domains.yaml](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/domains.png)
Note : Notice that preceding dot [ . ]

Lets take “.facebook.com” as example , domains extracted from Real time CT logs will be matched against the word “.facebook.com” , if matched they will be logged in our output file (found-domains.log) . The thing to note here is , It will give some false positives like “test.facebook.com.test.com” , “example.facebook.company” but we can filter out them later on by using use regex magic

#### For Matching domains/subdomains with specific keywords :

Lets assume that you want to monitor and log domains/subdomains that are having word “hackerone” in them , then our domains.yaml file will look something like this
![domains.yaml](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/keyword.png)
Now all the extracted domains/subdomains that are having word “hackerone” in them will be matched and logged (and a slack notification will be sent to you for the same)

Okay we are done with our initial setup , Lets install the required dependencies and run our tool

`$ pip3 install -r requirements.txt`

`$ python3 certeagle.py`

![](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/start.png)

**Matched domains will look like this :**

![](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/output.png)

**Slack Notifications will look like this :**

![enter image description here](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/slack.png)


**Output files :**

The program will keep on running all the matched domains will be saved under output directory in found-domains.log file

![](https://raw.githubusercontent.com/devanshbatham/CertEagle/master/static/found-domains.png)

**Strict Warning : Do not monitor assets of any organisation without prior consent**

### Inspriration 

[Sublert](https://github.com/yassineaboukir/sublert/) 

[Phishing Catcher](https://github.com/x0rz/phishing_catcher)

### Contact

Shoot my DM : [@0xAsm0d3us](https://twitter.com/0xAsm0d3us)

### #Offtopic but Important

This COVID pandemic affected animals too (in an indirect way) . I will be more than happy if you will show some love for Animals by donating to [Animal Aid Unlimited](https://animalaidunlimited.org/) ,[Animal Aid Unlimited](https://animalaidunlimited.org/) saves animals through street animal rescue, spay/neuter and education. Their mission is dedicated to the day when all living beings are treated with compassion and love. ✨
