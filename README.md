# Cisco Meraki Splash Page using Cisco Webex Connect

This code was created to demo the use case of leveraging Cisco Webex Connect (formally IMI Connect) to deliver the SMS authorization code to Guest Wifi users.

## Things to know about this code

1. In the `db.py` file, we're checking to see if the phone number is one that is in a list.  This was done for simple demo purpose to show that we could verify that a number isn't apart of an employee list.  This would be if a company didn't want employees jumping on to Guest Wifi to do business. 
1. We are using Redis for the DB to keep track of SMS codes and Phone Numbers.
1. I used [this tutoral](https://developer.cisco.com/meraki/captive-portal-api/#!click-through-api) for knowledge and [this javascript](https://github.com/dexterlabora/excap-clientjs) example to help with the logic. 
1. I'm using a Heroku account to make it available for testing with Meraki. 