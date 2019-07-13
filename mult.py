#!/usr/bin/env/python3
import paramiko
import os,sys,re,time
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a')
                    #filename='./log/check.log',
                    #filemode='w')

host_mme = '172.0.5.35'
host_4ggw = '172.0.5.36'
host_sgw = '172.0.5.37'
host_pgw = '172.0.5.38'
port = 22
username = 'root'
password = 'casa'

#cmd list
showmmeinfo = 'show mme info\r'
showtaskcrash = 'show task crash\r'
showhainfo = 'show ha info\r'

def run_cli(hostname,command,port=22):
    try:
        logging.info('The host {} is connecting!'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username=username,password=password)
        logging.info('Connect to host {} successful!'.format(hostname))
        channel = transport.open_session()
        channel.settimeout(3)
        channel.get_pty()   #模拟终端
        channel.invoke_shell()
        channel.send('/usr/local/bin/casa/casa-cli\n')  #login into cli mode 
        time.sleep(1)
        channel.send('page-off\r')
        time.sleep(1)
        logging.debug(channel.recv(65535).decode(encoding='utf-8')) #debug login info
        sys.stdout.flush()  #clear login info flush data
        channel.send(command)   #send the command
        time.sleep(3)
        context_bytes = channel.recv(65535)
        context = context_bytes.decode(encoding='utf-8')
        logging.debug(context)
        channel.close()
        transport.close()
        return context
    except Exception as e:
        logging.error('Try to connect host {} failure! The reason is {}'.format(hostname,e))

def comparsion(result,comparer):
    pattern = re.compile(comparer,re.M)
    comparsion = pattern.search(result)
    if comparsion:
        logging.info(result)
        logging.info('The result is Successful!')
    else:
        logging.error(result)
        logging.info('The result is Failure!')


if __name__ == '__main__':
    #check mme crash status
    cli_context = run_cli(host_mme,showtaskcrash)
    logging.info('Checking host {} system status:show task crash info'.format(host_mme))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    #check mme ha info
    cli_context = run_cli(host_mme,showhainfo)
    logging.info('Checking host {} system status:show ha info'.format(host_mme))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)

    #check mme info
    cli_context = run_cli(host_mme,showmmeinfo)
    logging.info('Checking host {} system status:show mme info'.format(host_mme))
    #logging.info(cli_context)
    comparer = 'service\sname\s+mme1'
    comparsion(cli_context,comparer)

    #check 4ggw crash status
    cli_context = run_cli(host_4ggw,showtaskcrash)
    logging.info('Checking host {} system status:show task crash info'.format(host_mme))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    #check 4ggw ha info
    cli_context = run_cli(host_4ggw,showhainfo)
    logging.info('Checking host {} system status:show ha info'.format(host_mme))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)

    #check sgw crash status
    cli_context = run_cli(host_sgw,showtaskcrash)
    logging.info('Checking host {} system status:show task crash info'.format(host_mme))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    #check sgw ha info
    cli_context = run_cli(host_sgw,showhainfo)
    logging.info('Checking host {} system status:show ha info'.format(host_mme))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)

    #check pgw crash status
    cli_context = run_cli(host_pgw,showtaskcrash)
    logging.info('Checking host {} system status:show task crash info'.format(host_mme))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    #check pgw ha info
    cli_context = run_cli(host_pgw,showhainfo)
    logging.info('Checking host {} system status:show ha info'.format(host_mme))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)
