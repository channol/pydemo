#!/usr/bin/python3
import paramiko
import os,sys,re,time
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt="%Y-%m-%d %H:%M:%S %a")

def copy_version(version,hostname,port=22):
    try:
        start = time.time()
        logging.info('start copy version from 172.0.5.90:/version/nfv-builds/')
        logging.info('login server {}'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username='root',password='casa')
        logging.info('login server {} successful'.format(hostname))
        channel = transport.open_session()
        #channel.settimeout(10)
        channel.get_pty()
        channel.invoke_shell()
        channel.send('/usr/local/bin/casa/casa-cli\n')
        time.sleep(3)
        result = (channel.recv(65535)).decode(encoding='utf-8')
        #logging.info(result)
        sys.stdout.flush()
        channel.send('enable\r')
        time.sleep(3)
        result = (channel.recv(65535)).decode(encoding='utf-8')
        #logging.info(result)
        pattern_password = re.compile('[Pp]assword:',re.M)
        comparsion = pattern_password.search(result)
        if comparsion:
            channel.send('casa\r')
            time.sleep(1)
            result = (channel.recv(65535)).decode(encoding='utf-8')
            #logging.info(result)
            sys.stdout.flush()
            channel.send('copy scp root 172.0.5.90 /version/nfv-builds/{}/casa-nfv-{}.tar.gz nvram\r'.format(version,version))
            time.sleep(1)
            result = (channel.recv(65535)).decode(encoding='utf-8')
            logging.info(result)
            comparsion1 = pattern_password.search(result)
            if comparsion1:
                channel.send('casa\r')
                logging.info('Waiting for copy file!!!')
                time.sleep(15)
                result = (channel.recv(65535)).decode(encoding='utf-8')
                logging.info(result)
                sys.stdout.flush()
                channel.send('md5 checksum casa-nfv-{}.tar.gz\r'.format(version))
                time.sleep(1)
                result2 = (channel.recv(65535)).decode(encoding='utf-8')
                #logging.info(result)
                pattern_md5 = re.compile('\s\scasa-nfv-{}.tar.gz'.format(version),re.M)
                comparsion2 = pattern_md5.search(result2)
                if comparsion2:
                    logging.info('the version {} file md5 checksum is:'.format(version))
                    logging.info(result2)
                    end = time.time()
                    logging.info('Spend time:{}'.format(end-start))
                else:
                    logging.info('The version file is no exist!')
                    end = time.time()
                    logging.info('Spend time:{}'.format(end-start))
            else:
                logging.error('Host {} can not copy version file'.format(hostname))
                result = (channel.recv(65535)).decode(encoding='utf-8')
                logging.info(result)
                end = time.time()
                logging.info('Spend time:{}'.format(end-start))
        else:
            logging.error('Host {} can not copy version file without enable mode'.format(hostname))
            result = (channel.recv(65535)).decode(encoding='utf-8')
            logging.info(result)
            end = time.time()
            logging.info('Spend time:{}'.format(end-start))

        channel.close()
        transport.close()
    except Exception as e:
        logging.error('Try to update host {} to version {} failure! The reason is {}'.format(hostname,version,e))

def update(version,hostname,port=22):
    try:
        logging.info('software update!')
        transport = paramiko.Transport(hostname,port)
        transport.connect(username='root',password='casa')
        logging.info('login server {} successful'.format(hostname))
        channel = transport.open_session()
        #channel.settimeout(10)
        channel.get_pty()
        channel.invoke_shell()
        channel.send('/usr/local/bin/casa/casa-cli\n')
        time.sleep(3)
        result = (channel.recv(65535)).decode(encoding='utf-8')
        #logging.info(result)
        sys.stdout.flush()
        channel.send('enable\r')
        time.sleep(3)
        result_enable = (channel.recv(65535)).decode(encoding='utf-8')
        #logging.info(result)
        pattern_password = re.compile('[Pp]assword:',re.M)
        comparsion = pattern_password.search(result_enable)
        if comparsion:
            channel.send('casa\r')
            time.sleep(1)
            result = (channel.recv(65535)).decode(encoding='utf-8')
            #logging.info(result)
            sys.stdout.flush()
            channel.send('system update casa-nfv-{}.tar.gz\r'.format(version))
            time.sleep(15)
            result_update = (channel.recv(65535)).decode(encoding='utf-8')
            logging.info(result_update)
            pattern_update = re.compile('System\supdate\shas\sbeen\sscheduled',re.M)
            comparsion1 = pattern_update.search(result_update)
            if comparsion1:
                logging.info('system update successful and should be reboot!')
            else:
                logging.error('The version is not failure!')
                logging.error(result_update)
        else:
            logging.error('It need enable mode to update version!!!')
            logging.error(result_enable)

        channel.close()
        transport.close()
    except Exception as e:
        logging.error('Try to update host {} to version {} failure! The reason is {}'.format(hostname,version,e))

if __name__ == '__main__':
#    hostname = input('enter update hostname:')
#    time.sleep(1)
#    version = input('enter update version:')
#    time.sleep(1)
    hostname = '172.0.10.165'
    version = '4.9.3-319'
    port = 22
    copy_version(version,hostname)
    update(version,hostname)


