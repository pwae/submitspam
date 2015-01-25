# Submit Spam

## Setting it up in Postfix.

Start by adding the following to Postfix' `main.cf` (if it doesn't already exist):

    transport_maps=hash:/etc/postfix/transport

Next, in the file `/etc/postfix/transport`, add a line similar to the below:

  **spam@submit.local** submitspam:localhost

You should change the email address at the beginning, to something unique and private that no one can guess.
After that, you should compile the file into a hash file for postfix with the following command:

  sudo postmap /etc/postfix/transport

This will create `/etc/postfix/transport.db`. 
Following that, update `/etc/postfix/master.cf` to have a line like below:

  submitspam unix   -       n       n       -       1       pipe
  flags= user=**debian-spamd** argv=**/opt/spam/submitspam/submitspam.py**

You should update the user to be whatever user your spam assassin processes run as. On Ubuntu/debian, it is debian-spamd.
Also update the path to the script as required.

Once this is done, just issue a reload to postfix:

  sudo postfix reload

... and then it should all be working. Try sending an email with an email attachment to classify as spam to that email address in Postfix, and see how you go!
