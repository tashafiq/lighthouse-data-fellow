"""
Extract selected mails from your gmail account

1. Make sure you enable IMAP in your gmail settings
(Log on to your Gmail account and go to Settings, See All Settings, and select
 Forwarding and POP/IMAP tab. In the "IMAP access" section, select Enable IMAP.)

2. If you have 2-factor authentication, gmail requires you to create an application
specific password that you need to use.
Go to your Google account settings and click on 'Security'.
Scroll down to App Passwords under 2 step verification.
Select Mail under Select App. and Other under Select Device. (Give a name, e.g., python)
The system gives you a password that you need to use to authenticate from python.

"""

# Importing libraries
import imaplib
import email as email
import yaml as yaml  # To load saved login credentials from a yaml file #yml-1.3#

with open("credentials.yml") as f:
    content = f.read()

# from credentials.yml import user name and password
my_credentials = yaml.load(content, Loader=yaml.FullLoader)

# Load the user name and passwd from yaml file
user, password = my_credentials["user"], my_credentials["password"]

# URL for IMAP connection
imap_url = 'imap.gmail.com'

# Connection with GMAIL using SSL
my_mail = imaplib.IMAP4_SSL(imap_url)

# Log in using your credentials
my_mail.login(user, password)

# Select the Inbox to fetch messages
my_mail.select('Inbox')

# Define Key and Value for email search
# For other keys (criteria): https://gist.github.com/martinrusev/6121028#file-imap-search
key = 'FROM'
value = 'LTB@ontario.ca'
_, data = my_mail.search(None, key, value)  # Search for emails with specific key and value

mail_id_list = data[0].split()  # IDs of all emails that we want to fetch

msgs = []  # empty list to capture all messages
# Iterate through messages and extract data into the msgs list
for num in mail_id_list:
    typ, data = my_mail.fetch(num, '(RFC822)')  # RFC822 returns whole message (BODY fetches just body)
    msgs.append(data)

# Now we have all messages, but with a lot of details
# Let us extract the right text and print on the screen

# In a multipart e-mail, email.message.Message.get_payload() returns a
# list with one item for each part. The easiest way is to walk the message
# and get the payload on each part:
# https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

# NOTE that a Message object consists of headers and payloads.

#Files to write to
file = open('data.txt', 'a')

for msg in msgs[::-1]:
    for response_part in msg:
        if type(response_part) is tuple:
            my_msg = email.message_from_bytes((response_part[1]))
            file.write("_________________________________________\n")
            file.write("subj:+" +str(my_msg['subject']) +'\n')
            file.write("from:+" +str(my_msg['from']) +'\n')
            file.write("date:+" +str(my_msg['date']) +'\n')
            for part in my_msg.walk():
                if part.get_content_type() == 'text/plain':
                    #We'll use the base64 package's decoder: https://stackoverflow.com/questions/38970760/how-to-decode-a-mime-part-of-a-message-and-get-a-unicode-string-in-python-2
                    bytes = part.get_payload(decode=True)
                    charset = part.get_content_charset('iso-8859-1')
                    chars = bytes.decode(charset, 'replace')
                    #Now we have the email body as a string, from which we can pull our relevant data
                    body = chars.split()
                    hearing_count = 0
                    urgent_count = 0
                    adjourned_count = 0
                    for i in range(0,len(body)-1):
                        if body[i] == 'Zoom' and body[i+1] == 'Link:':
                            hearing_count += 1
                        if body[i] == 'Urgent' and body[i+1] == '–':
                            urgent_count += 1
                        if body[i] == 'Adjourned' and body[i+1] == 'Block':
                            adjourned_count = 0
                    " ".join(body)
                    file.write(str(body) + '\n')
                    file.write('\n')
                    file.write("total hearings this week:" + str(hearing_count) + '\n')
                    file.write("urgent hearings:" + str(urgent_count) + '\n')                
                    file.write("adjourned hearings:" + str(adjourned_count) + '\n')