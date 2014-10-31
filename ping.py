import os
import datetime
import time
import send_email

FROM_ADDRESS = 'titanicping@fire.caltech.edu'
TO_ADDRESSES = 'feldmando+m@gmail.com, feldmando+titanicping@gmail.com'
# Do not send an email if we sent an email within the last DELAY_TIME seconds.
DELAY_TIME = 172800
last_email_time_file = 'last_email_time.txt'
server_to_ping = 'titanic.caltech.edu'


def ping(hostname):
    response = os.system('ping -c 1 ' + hostname)
    if response != 0:
        humantime = str(datetime.datetime.now())
        epochtime = time.time()
        last_email_time = 0
        try:
            with open(last_email_time_file, 'rb') as f:
                last_email_time = float(f.read().strip())
        except IOError:
            with open(last_email_time_file, 'wb') as f:
                f.write('0')
        if epochtime - last_email_time > DELAY_TIME:
            send_email.send(
                    FROM_ADDRESS,
                    TO_ADDRESSES,
                    'Ping to %s failed' % hostname,
                    humantime)
            with open(last_email_time_file, 'wb') as f:
                f.write(str(epochtime))


if __name__ == '__main__':
    ping(server_to_ping)
