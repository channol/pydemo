#!/usr/bin/python3

import paramiko
import os,time,re,sys
import logging

def dockerip(hostname,port=22):
    try:
        logging.info('connecting host {} ...'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username='root',password='casa')
        logging.info('Connecting host {} is successful!'.format(hostname))
        channel = transport.open_session()
        channel.settimeout(3)
        channel.get_pty()
        channel.invoke_shell()
        time.sleep(1)
        channel.send('docker ps\n')
        time.sleep(1)
        result = channel.recv(65535).decode(encoding='utf-8')
        #logging.info(result)
        pattern = re.compile('root.[a-z]+_[a-z]+_[1-9]')
        result_list = pattern.findall(result)
        #logging.info(result_list)
        if result_list:
            print('docker ip is:')
            for pop in result_list:
                sys.stdout.flush()
                dockeriper = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'"
                channel.send('{} {}\n'.format(dockeriper,pop))
                time.sleep(1)
                result_pop = channel.recv(65535).decode(encoding='utf-8')
                pattern_ip = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
                pop_ip = pattern_ip.search(result_pop)
                print(pop,pop_ip.group())
        else:
            logging.info('no find pop!')

        channel.close()
        transport.close()

    except Exception as err:
        logging.info('Connecting host {} is failure!!! Reason is {}'.format(hostname,err))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')

    hostname='172.0.5.27'
    port=22

    dockerip(hostname,port)


