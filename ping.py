import os
import datetime
import time
import send_email

FROM_ADDRESS = 'titanicping@fire.caltech.edu'
TO_ADDRESSES = open('notify_these_addresses.txt').read().strip()
# Do not send an email if we sent an email within the last DELAY_TIME seconds.
DELAY_TIME = 172800
last_email_time_file = 'last_email_time.txt'
server_to_ping = 'titanic.caltech.edu'


def ping_with_retries(hostname, max_tries, wait_seconds=60):
    humantime1 = str(datetime.datetime.now())
    num_tries = 0
    # While ping fails
    while os.system('ping -c 1 ' + hostname) != 0:
        num_tries += 1
        if num_tries < max_tries:
            time.sleep(wait_seconds)
        else:
            break
    if num_tries < max_tries:
        # Ping eventually succeeded
        return True
    humantime2 = str(datetime.datetime.now())
    epochtime2 = time.time()
    return humantime1, humantime2, epochtime2


def test(hostname):
    max_tries = 3
    response = ping_with_retries(hostname, max_tries)
    if response is True:
        return
    humantime1, humantime2, epochtime2 = response
    last_email_time = 0
    try:
        with open(last_email_time_file, 'rb') as f:
            last_email_time = float(f.read().strip())
    except IOError:
        with open(last_email_time_file, 'wb') as f:
            f.write('0')
    if epochtime2 - last_email_time > DELAY_TIME:
        message = open('message.txt', 'rb').read().strip()
        message = message.format(max_tries, humantime1, humantime2)
        send_email.send(
                FROM_ADDRESS,
                TO_ADDRESSES,
                'Ping to %s failed' % hostname,
                message)
        with open(last_email_time_file, 'wb') as f:
            f.write(str(epochtime2))


if __name__ == '__main__':
    test(server_to_ping)
