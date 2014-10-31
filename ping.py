import os
import datetime
import time
import send_email

FROM_ADDRESS = 'titanicping@fire.caltech.edu'
TO_ADDRESSES = 'feldmando+m@gmail.com, feldmando+titanicping@gmail.com'
DELAY_TIME = 172800  # in seconds


def ping(hostname):
    response = os.system('ping -c 1 ' + hostname)
    if response != 0:
        humantime = str(datetime.datetime.now())
        epochtime = time.time()
        with open('last_email_time.txt', 'rb') as f:
            last_email_time = float(f.read().strip())
        if epochtime - last_email_time > DELAY_TIME:
            send_email.send(
                    FROM_ADDRESS,
                    TO_ADDRESSES,
                    'Ping to %s failed' % hostname,
                    humantime)
            with open('last_email_time.txt', 'wb') as f:
                f.write(str(epochtime))


if __name__ == '__main__':
    ping('titanic.caltech.edu')
