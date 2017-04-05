#!/usr/bin/env python

"""
This is a littel sample app that sends an email via gmail

I've set up a gmail account for the class, so we don't have
to worry about security on our personal accounts!

class gmail account:

login: uwpcepythoncert
password: ChrisAndMaria

Birthday, if it ever comes up (not sure why it would)
April 4 2000

NOTE: This example uses the less secure plain text login -- it's easier.

But I had to turn on "Allow less secure apps" in gmail for it to work.

Here is a quickstart:

https://developers.google.com/gmail/api/quickstart/python

you will need the google client API client

pip install --upgrade google-api-python-client

"""

import gmail_api

# # Here is the smtp way -- but I couldn't get it to login successfully

# import smtplib  # the built-in email sending client

# # gmail_user = "uwpcepythoncert@gmail.com"
gmail_user = "uwpcepythoncert"

# gmail_password = "ChrisAndMaria"

# # try:
# #     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# #     server.ehlo()
# #     server.login(gmail_user, gmail_password)
# #     print("successful login")
# # except smtplib.SMTPAuthenticationError:
# #     print('Something went wrong...')
# #     raise

# # server = smtplib.SMTP('smtp.gmail.com', 587)
# # server.starttls()
# # server.login(gmail_user, gmail_password)

# # msg = "This is a very simple message"
# # server.sendmail("YOUR EMAIL ADDRESS", "PythonCHB@gmail.com", msg)
# # server.quit()

def create_message(sender, to, subject, message_text):
  """
  Create a message for an email. for gmail API

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

test_msg = create_message("python class",
                          "PythonCHB@gmail.com",
                          "test email",
                          "This is an example message")

# get the service...
creds = gmail_api.get_credentials()

    credentials = gmail_api.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)


send_message(service,
             gmail_user,
             test_message)




