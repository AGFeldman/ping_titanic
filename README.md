The ping.py script pings a server and sends an email if the ping fails. 

The script is intended to be run as a cron job from a machine with an SMTP server set up. You can set up an SMTP server with `sudo aptitude install postfix`.

The ping.py script creates the file last_email_time.txt to store the time, in seconds since epoch, when the most recent notification email was sent.
