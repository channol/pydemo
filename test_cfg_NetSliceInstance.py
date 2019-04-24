# This script could be used for actix-web CASA 5G protocol test
# just start server and run test_client.py
# Originor Author: N/A 
# Second Author: zhixiang chen
# Date: 01/08/2019
# Version 1.0
# Purpose: this scripts replace the manul curl test.
# Once you finished the API, you may use this scripts to conduct the test.
# In general, you need appand into the test_path, in what is called dictionary data structure in Python, and add your own test_package. 
# Remember: this is a python program, once the bool defined in Rust program suchlike 1, false,
# You must translate 1, False at which python program accepts.
# to run this scripts: python3 test_uecm.py
# For run, You most likely at very first need install third party lib
# pip3 install <package>    

import json
import asyncio
import aiohttp
import requests
from config import *

SERVER_IP = "172.0.4.138"
SERVER_PORT= "8008"

DEFAULT_HTTP_PATH='http://'+SERVER_IP+':'+SERVER_PORT

cfg_path = {
    1: '/casa-dbg/dummy-dump',
    2: '/casa-admin/db-init',
# post/get NSI
    3: '/nssf-mgmt/config-network-slice-instance',
# get/delete NSI
    4: '/nssf-mgmt/show-network-slice-instance',
    5: '/nssf-mgmt/delete-network-slice-instance',
# post/get CSNssai
    6: '/nssf-configure/v1/csnssai',
# get/delete CSNssai
    7: '/nssf-configure/v1/csnssai?snssai={"sst":1,"sd":"abd001"}',
# get plmn restricted-snssai
    8: '/nssf-configure/v1/plmn-restricted-snssai?plmn-id={"mcc":"911","mnc":"492"}',
# get ta restricted-snssai
    9: '/nssf-configure/v1/ta-restricted-snssai?tai={"plmnId":{"mcc":"811","mnc":"494"},"tac":"tac811"}',
    # post/get incorrect NSI URI
    10: '/nssf-mgmt/config-network-slice-instance/1',
    # get/delete not exist nsiId
    11: '/nssf-configure/v1/network-slice-instance/10',
    # show nsiId with incorrect URI
    12: '/nssf-mgmt/show-network-slice-instance/1',
    # delete nsiId with incorrect URI and don't exist nsiId
    13: '/nssf-mgmt/delete-network-slice-instance/1',
}

cfg_pkg = {
# NetSliceInstance 1
    1: {"sNssai":[{"sst":1,"sd":"abd001"},{"sst":1,"sd":"sd6456"}],
        "nfSets":[{"setId":"set1","nfType":"AMF","nfId":["9104871234151","amf-1","AMF-1","AMF_1"]},
            {"setId":"set2","nfType":"SMF","nfId":["smf-1","SMF-1","SMF_1"]},
            {"setId":"set3","nfType":"NRF","nfId":["nrf-1","NRF-1","NRF_1"]}],
        "ratType":["NR","EUTRA","WLAN","VIRTUAL"],
        "default":True,"supportedFeatures":"910abcd"},  
# NetSliceInstance 2 (add other parameters)
    2: {"sNssai":[{"sst":2,"sd":"abd002"}],
        "nfSets":[{"setId":"set2","nfType":"AMF","nfId":["9104871234152","amf-2"]}],
        "ratType":["NR","EUTRA","WLAN","VIRTUAL"],"data":"just_test","plmnid":"mccnc",
        "default":True,"supportedFeatures":"910abcd"},
# NetSliceInstance 3 (just one parameter)
    3: {"sNssai":[{"sst":3,"sd":"abd003"}]},
# NetSliceInstance 4 (just two parameters)
    4: {"sNssai":[{"sst":4,"sd":"abd004"}],
        "nfSets":[{"setId":"set4","nfType":"AMF","nfId":["9104871234154","amf-4"]}]},
# NetSliceInstance 5 (three parameters)
    5: {"sNssai":[{"sst":5,"sd":"abd005"}],
        "nfSets":[{"setId":"set5","nfType":"AMF","nfId":["9104871234155","amf-5"]}],
        "ratType":["NR","EUTRA","WLAN","VIRTUAL"]},
# NetSliceInstance 6 (three parameters)
    6: {"sNssai":[{"sst":6,"sd":"abd006"}],
        "nfSets":[{"setId":"set6","nfType":"AMF","nfId":["9104871234156","amf-6"]}],
        "ratType":["NR","EUTRA","WLAN","VIRTUAL"],"default":True},

#NSIID
    7: {"id":"1"},
    8: {"id":"100"},
    9: {"id":"2"},
    10: {"id":"3"},

# NetSliceInstance 2
    12: {"sNssai":[{"sst":1,"sd":"abd002"},{"sst":1,"sd":"sd6456"}],"nfSets":[{"setId":"set1","nfType":"AMF","nfId":["9104871234151","amf-1","AMF-1","AMF_1"]},{"setId":"set2","nfType":"SMF","nfId":["smf-1","SMF-1","SMF_1"]},{"setId":"set3","nfType":"NRF","nfId":["nrf-1","NRF-1","NRF_1"]}],"ratType":["NR","EUTRA","WLAN","VIRTUAL"],"default":False,"supportedFeatures":"910abcd"},
# SCNssai
    13: {"snssai":{"sst":1,"sd":"abd001"},"hPlmnId":[{"plmnId":{"mcc":"910","mnc":"487"},"restricted":False,"restrictedTai":[{"plmnId":{"mcc":"811","mnc":"491"},"tac":"tac811"},{"plmnId":{"mcc":"811","mnc":"492"},"tac":"tac811"}]},{"plmnId":{"mcc":"910","mnc":"488"},"restricted":True,"restrictedTai":[]}],"sPlmnId":[{"plmnId":{"mcc":"911","mnc":"491"},"homeSnssai":{"sst":2,"sd":"abd002"},"restricted":False,"restrictedTai":[{"plmnId":{"mcc":"811","mnc":"493"},"tac":"tac811"},{"plmnId":{"mcc":"811","mnc":"494"},"tac":"tac811"}]},{"plmnId":{"mcc":"911","mnc":"492"},"homeSnssai":{"sst":3,"sd":"abd003"},"restricted":True,"restrictedTai":[]}],"restrictedTai":[{"plmnId":{"mcc":"811","mnc":"491"},"tac":"tac811"},{"plmnId":{"mcc":"811","mnc":"492"},"tac":"tac811"}],"ratType":["NR","EUTRA","WLAN","VIRTUAL"],"supportedFeatures":"910abcd"},
    14: {"maxNsi":3,"method":"First"},
}

POST = "post"
PUT = "put"
GET = "get"
DELETE = "delete"
PATCH = "patch"

def test_db_init():
    path = DEFAULT_HTTP_PATH + cfg_path[2]
    print('Request Info -----')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            PUT, path)

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

# Post NSI
###1.001 Configure_server post netsliceinstance with correct URI and full parameters on body_content(include 'sNssai', 'nfSets', 'ratType', 'default', 'supportedFeatures'), 
### NSSF response 200 status code and NSIID on content.###
def test_cfg_post_nsi_1():
    path = DEFAULT_HTTP_PATH + cfg_path[3]
    print('Request Info -----cfg_path[3]')
    print(str(path))
    print('Request Body -----cfg_pkg[1]')
    print(str(cfg_pkg[1]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[1]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###1.002 Configure_server post netsliceinstance with correct URI and additional parameters on body_content(include 'sNssai', 'nfSets', 'ratType', 'default', 'supportedFeatures', add other parameters such as 'plmnid' and so on)###
def test_cfg_post_nsi_2():
    path = DEFAULT_HTTP_PATH + cfg_path[3]
    print('Request Info -----cfg_path[3]')
    print(str(path))
    print('Request Body -----cfg_pkg[2]')
    print(str(cfg_pkg[2]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[2]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###1.003 Configure_server post netsliceinstance with incorrect URI and full body_content(include 'sNssai', 'nfSets', 'ratType', 'default', 'supportedFeatures'), NSSF response 404 status code.###
def test_cfg_post_nsi_3():
    path = DEFAULT_HTTP_PATH + cfg_path[10]
    print('Request Info -----cfg_path[10]')
    print(str(path))
    print('Request Body -----cfg_pkg[1]')
    print(str(cfg_pkg[1]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[1]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###1.004 Configure_server post netsliceinstance with correct URI and some parameters on body_content(include 'sNssai')###
def test_cfg_post_nsi_4():
    path = DEFAULT_HTTP_PATH + cfg_path[3]
    print('Request Info -----cfg_path[3]')
    print(str(path))
    print('Request Body -----cfg_pkg[3]')
    print(str(cfg_pkg[3]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[3]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert (404 == resp.status or 400 == resp.status)
    asyncio.get_event_loop().run_until_complete(method())

###1.005 Configure_server post netsliceinstance with correct URI and some parameters on body_content(include 'sNssai', 'nfSets')###
def test_cfg_post_nsi_5():
    path = DEFAULT_HTTP_PATH + cfg_path[3]
    print('Request Info -----cfg_path[3]')
    print(str(path))
    print('Request Body -----cfg_pkg[4]')
    print(str(cfg_pkg[4]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[4]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert (404 == resp.status or 400 == resp.status)
    asyncio.get_event_loop().run_until_complete(method())

###1.006 Configure_server post netsliceinstance with correct URI and some parameters on body_content(include 'sNssai', 'nfSets', 'ratType')###
def test_cfg_post_nsi_6():
    path = DEFAULT_HTTP_PATH + cfg_path[3]
    print('Request Info -----cfg_path[3]')
    print(str(path))
    print('Request Body -----cfg_pkg[5]')
    print(str(cfg_pkg[5]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[5]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert (404 == resp.status or 400 == resp.status)
    asyncio.get_event_loop().run_until_complete(method())

###1.007 Configure_server post netsliceinstance with correct URI and some parameters on body_content(include 'sNssai', 'nfSets', 'ratType','default')###
def test_cfg_post_nsi_7():
    path = DEFAULT_HTTP_PATH + cfg_path[3]
    print('Request Info -----cfg_path[3]')
    print(str(path))
    print('Request Body -----cfg_pkg[6]')
    print(str(cfg_pkg[6]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[6]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###1.008 Configure_server post the same netsliceinstance, NSSF response 200 status code and NSIID&NSI-info(the same with the previous NSIID) on content.###
def test_cfg_post_nsi_8():
    path = DEFAULT_HTTP_PATH + cfg_path[3]
    print('Request Info -----cfg_path[3]')
    print(str(path))
    print('Request Body -----cfg_pkg[6]')
    print(str(cfg_pkg[6]))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[6]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())


# # Post show NSI
###2.001 Configure_server post(show) netsliceinstance with correct URI (the nsiID exist on nssf), NSSF response 200 status code and NetSliceInstance info.###
def test_cfg_show_nsi_1():
    path = DEFAULT_HTTP_PATH + cfg_path[4]
    print('Request Info -----cfg_path[4]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[7]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###2.002 Configure_server post(show) netsliceinstance with correct URI (the nsiID don't exist on nssf), NSSF response 404 status code and content include 'NSI Not Found'###
def test_cfg_show_nsi_2():
    path = DEFAULT_HTTP_PATH + cfg_path[4]
    print('Request Info -----cfg_path[4]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[8]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###2.003 Configure_server post(show) netsliceinstance with incorrect URI (the nsiID exist on nssf), NSSF response 404 status code.###
def test_cfg_show_nsi_3():
    path = DEFAULT_HTTP_PATH + cfg_path[12]
    print('Request Info -----cfg_path[12]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[7]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###2.004 Configure_server post(show) netsliceinstance with incorrect URI (the nsiID don't exist on nssf), NSSF response 404 status code.###
def test_cfg_show_nsi_4():
    path = DEFAULT_HTTP_PATH + cfg_path[12]
    print('Request Info -----cfg_path[12]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[8]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

# # Delete NSI
###3.001 Configure_server delete netsliceinstance with correct URI (the nsi exist on nssf), NSSF response 200 status code.###
def test_cfg_delete_nsi_1():
    path = DEFAULT_HTTP_PATH + cfg_path[5]
    print('Request Info -----cfg_path[5]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[7]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###3.002 After delete netsliceinstance on nssf, Configure_server show netsliceinstance with the previous nsiID, NSSF response 404 status code.###
def test_cfg_show_nsi_5():
    path = DEFAULT_HTTP_PATH + cfg_path[4]
    print('Request Info -----cfg_path[4]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[7]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###3.003 Configure_server delete netsliceinstance with correct URI (the nsi don't exist on nssf), NSSF response 404 status code.###
def test_cfg_delete_nsi_2():
    path = DEFAULT_HTTP_PATH + cfg_path[5]
    print('Request Info -----cfg_path[5]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[8]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###3.004 Configure_server delete netsliceinstance with incorrect URI (the nsi exist on nssf), NSSF response 404 status code.###
def test_cfg_delete_nsi_3():
    path = DEFAULT_HTTP_PATH + cfg_path[13]
    print('Request Info -----cfg_path[13]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[7]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

###3.005 Configure_server delete netsliceinstance with incorrect URI (the nsi don't exist on nssf), NSSF response 404 status code.###
def test_cfg_delete_nsi_4():
    path = DEFAULT_HTTP_PATH + cfg_path[13]
    print('Request Info -----cfg_path[13]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[8]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 404 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

################################################# delete records from DB ###################################################
def test_cfg_delete_nsi_5():                      ##relate to case 1.002##
    path = DEFAULT_HTTP_PATH + cfg_path[5]
    print('Request Info -----cfg_path[5]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[9]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())

def test_cfg_delete_nsi_6():                      ##relate to case 1.007##
    path = DEFAULT_HTTP_PATH + cfg_path[5]
    print('Request Info -----cfg_path[5]')
    print(str(path))

    async def method():
        resp = await aiohttp.ClientSession().request(
            POST, path,
            data=json.dumps(cfg_pkg[10]),
        headers={"content-type": "application/json"})

        print('Response Info -----')
        print(str(resp))
        print('Response Body -----')
        print(await resp.text())
        assert 200 == resp.status
    asyncio.get_event_loop().run_until_complete(method())


