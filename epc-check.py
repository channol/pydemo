#!/usr/bin/env/python3
import paramiko
import os,sys,re,time
import logging
import configparser

#logging settin
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')

#set file handler of logging
#file_handler = logging.FileHandler('./log/{}.log'.format(time.strftime('%Y_%m_%d_%H_%M_%S')),mode='w')
file_handler = logging.FileHandler('./log/epc-check.log',mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a'))
logger.addHandler(file_handler)

#set console handler of logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a'))
logger.addHandler(console_handler)

#host paramer
config = configparser.ConfigParser()
config.read('./config/epc.config')
host_mme = config.get('login','host_mme')
host_4ggw = config.get('login','host_4ggw')
host_sgw = config.get('login','host_sgw')
host_pgw  = config.get('login','host_pgw')
port = config.get('login','port')
username = config.get('login','username')
password = config.get('login','password')

#cmd list
#showMmeInfo = 'show mme info\r'
showMmeInfo = config.get('cli','showMmeInfo')
showTaskCrash = config.get('cli','showTaskCrash')
showHaInfo = config.get('cli','showHaInfo')
showSgwcPfcp = config.get('cli','showSgwcPfcp')
showPgwcPfcp = config.get('cli','showPgwcPfcp')
showSgwcSessionSummary = config.get('cli','showSgwcSessionSummary')
showSgwuPfcp = config.get('cli','showSgwuPfcp')
showUpfPfcp = config.get('cli','showUpfPfcp')
showUpfSessionCounter = config.get('cli','showUpfSessionCounter')
showUpfSession = config.get('cli','showUpfSession')
showLteServiceHenbGatewayHenbInterface = config.get('cli','showLteServiceHenbGatewayHenbInterface')


def run_cli(hostname,command,port=22):
    try:
        logging.info('The host {} is connecting!'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username=username,password=password)
        logging.info('Connect to host {} successful!'.format(hostname))
        channel = transport.open_session()
        channel.settimeout(3)
        channel.get_pty()
        channel.invoke_shell()
        channel.send('/usr/local/bin/casa/casa-cli\n')  #login into cli mode 
        time.sleep(1)
        channel.send('page-off\r')
        time.sleep(1)
        logging.debug(channel.recv(65535).decode(encoding='utf-8')) #debug login info
        sys.stdout.flush()  #clear login info flush data
        channel.send(command)   #send the command
        channel.send('\r')
        time.sleep(3)
        context_bytes = channel.recv(65535)
        context = context_bytes.decode(encoding='utf-8')
        logging.debug(context)
        channel.close()
        transport.close()
        return context
    except Exception as e:
        logging.error('Try to connect host {} failure! The reason is {}'.format(hostname,e))

def comparsion(result,*comparer):
    for comp in comparer:
        pattern = re.compile(comp,re.M)
        comparsion = pattern.search(result)
        if comparsion is None:
            logging.error(result)
            logging.error('******The result is Failure! The matcher is {}'.format(comp))
            break
        else:
            logging.info('Checking step {} is successful!'.format(comparsion))
            continue



if __name__ == '__main__':
    start = time.time()
    logging.info('beginning check mme crash status')
    cli_context = run_cli(host_mme,showTaskCrash)
    logging.info('Checking host {} system status:{}'.format(host_mme,showTaskCrash))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    logging.info('beginning check mme ha info')
    cli_context = run_cli(host_mme,showHaInfo)
    logging.info('Checking host {} system status:{}'.format(host_mme,showHaInfo))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)

    logging.info('beginning check mme info')
    cli_context = run_cli(host_mme,showMmeInfo)
    logging.info('Checking host {} system status:{}'.format(host_mme,showMmeInfo))
    comparer = 'service\sname\s+mme1'
    comparer1 = 's1ap\sconnections\s+[0-9]*[1-9][0-9]*'
    comparer2 = 'sctp\sassociations\s+[0-9]*[1-9][0-9]*'
    comparsion(cli_context,comparer,comparer1,comparer2)
    logging.info(cli_context)


    logging.info('beginning check 4ggw info')
    cli_context = run_cli(host_4ggw,showTaskCrash)
    logging.info('Checking host {} system status:{}'.format(host_4ggw,showTaskCrash))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    logging.info('beginning check 4ggw ha info')
    cli_context = run_cli(host_4ggw,showHaInfo)
    logging.info('Checking host {} system status:{}'.format(host_4ggw,showHaInfo))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)

    logging.info('beginning check {}'.format(showLteServiceHenbGatewayHenbInterface))
    cli_context = run_cli(host_4ggw,showLteServiceHenbGatewayHenbInterface)
    logging.info('Checking host {} system status:{}'.format(host_4ggw,showLteServiceHenbGatewayHenbInterface))
    comparer = 'global-enb-id\s+:\smcc\s311,\smnc\s480,\shome-enb-id\s400'
    comparer1 = 'global-enb-id\s+:\smcc\s311,\smnc\s480,\shome-enb-id\s401'
    comparsion(cli_context,comparer,comparer1)
    logging.info(cli_context)

    logging.info('beginning check sgw crash info')
    cli_context = run_cli(host_sgw,showTaskCrash)
    logging.info('Checking host {} system status:{}'.format(host_sgw,showTaskCrash))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    logging.info('beginning check sgw ha info')
    cli_context = run_cli(host_sgw,showHaInfo)
    logging.info('Checking host {} system status:{}'.format(host_sgw,showHaInfo))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)

    logging.info('beginning check sgwc pfcp info')
    cli_context = run_cli(host_sgw,showSgwcPfcp)
    logging.info('Checking host {} system status:{}'.format(host_sgw,showSgwcPfcp))
    comparer = 'Peer\sNode\sType\s:\sPFCP_SGW_UP\s+State\s:\sConnected'
    comparsion(cli_context,comparer)

    logging.info('beginning check pgwc pfcp info')
    cli_context = run_cli(host_sgw,showPgwcPfcp)
    logging.info('Checking host {} system status:{}'.format(host_sgw,showPgwcPfcp))
    comparer = 'Peer\sNode\sType\s:\sPFCP_PGW_UP\s+State\s:\sConnected'
    comparsion(cli_context,comparer)

    logging.info('beginning check {}'.format(showSgwcSessionSummary))
    cli_context = run_cli(host_sgw,showSgwcSessionSummary)
    logging.info('Checking host {} system status:{}'.format(host_sgw,showSgwcSessionSummary))
    logging.info(cli_context)

    logging.info('beginning check pgw task crash info')
    cli_context = run_cli(host_pgw,showTaskCrash)
    logging.info('Checking host {} system status:{}'.format(host_pgw,showTaskCrash))
    comparer = '[Tt]otal\s0\scrash\srecords'
    comparsion(cli_context,comparer)

    logging.info('beginning check pgw ha info')
    cli_context = run_cli(host_pgw,showHaInfo)
    logging.info('Checking host {} system status:{}'.format(host_pgw,showHaInfo))
    comparer = 'state\s+:\sActive'
    comparsion(cli_context,comparer)


    logging.info('beginning check {}'.format(showSgwuPfcp))
    cli_context = run_cli(host_pgw,showSgwuPfcp)
    logging.info('Checking host {} system status:{}'.format(host_pgw,showSgwuPfcp))
    comparer = 'Peer\sNode\sType\s:\sPFCP_SGW_CP\s+State\s:\sConnected'
    comparsion(cli_context,comparer)

    logging.info('beginning check {}'.format(showUpfPfcp))
    cli_context = run_cli(host_pgw,showUpfPfcp)
    logging.info('Checking host {} system status:{}'.format(host_pgw,showUpfPfcp))
    comparer = 'Peer\sNode\sType\s:\sPFCP_PGW_CP\s+State\s:\sConnected'
    comparsion(cli_context,comparer)

    logging.info('beginning check {}'.format(showUpfSession))
    cli_context = run_cli(host_pgw,showUpfSession)
    logging.info('Checking host {} system status:{}'.format(host_pgw,showUpfSession))
    logging.info(cli_context)

    logging.info('beginning check {}'.format(showUpfSessionCounter))
    cli_context = run_cli(host_pgw,showUpfSessionCounter)
    logging.info('Checking host {} system status:{}'.format(host_pgw,showUpfSessionCounter))
    logging.info(cli_context)

    end = time.time()
    logging.info('Spend time: {}'.format(end-start))
