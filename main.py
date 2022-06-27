import requests, sys, time
sys.path.append('../..')
import go

def CheckAndGetSettings(meta_data):
    setting = meta_data.get('groupSettings')
    if setting.get('MCSMApi') and setting.get('MCSMUuid') and setting.get('MCSMKey') and setting.get('MCSMRemote'):
        return setting
    else:
        go.send(meta_data, '请先绑定服务器！')
        return 404

def hum_convert(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size

def state(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    setting = CheckAndGetSettings(meta_data)
    if setting == 404:
        return
    
    dataa = requests.get(url='{0}/api/instance?uuid={1}&remote_uuid={2}&apikey={3}'.format(setting.get('MCSMApi'), setting.get('MCSMUuid'), setting.get('MCSMRemote'), setting.get('MCSMKey')))
    datajson = dataa.json()
    
    if datajson['status'] == 200:
        data = '[CQ:face,id=161] 实例ID：'+datajson['data']['instanceUuid']+'\n[CQ:face,id=161] 当前状态：'+str(datajson['data']['status'])+'\n[CQ:face,id=161] 服务器名称：'+str(datajson['data']['config']['nickname'])+'\n[CQ:face,id=161] 服务器类型：'+str(datajson['data']['config']['type'])+'\n[CQ:face,id=161] 在线人数：'+str(datajson['data']['info']['currentPlayers'])+'\n[CQ:face,id=161] 最大人数：'+str(datajson['data']['info']['maxPlayers'])
    else:
        data = '[CQ:face,id=151] 执行失败！\n原因：'+datajson.get('data')+'\n执行时间：'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(datajson['time']))
    go.send(meta_data, data)

def stop(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    setting = CheckAndGetSettings(meta_data)
    if setting == 404:
        return
    
    dataa = requests.get(url='{0}/api/protected_instance/stop?uuid={1}&remote_uuid={2}&apikey={3}'.format(setting.get('MCSMApi'), setting.get('MCSMUuid'), setting.get('MCSMRemote'), setting.get('MCSMKey')))
    datajson = dataa.json()
    
    if datajson['status'] == 200:
        data = '[CQ:face,id=161] 执行成功！\n执行的实例：'+datajson['data']['instanceUuid']+'\n执行时间：'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(datajson['time']))
    else:
        data = '[CQ:face,id=151] 执行失败！\n原因：'+datajson.get('data')+'\n执行时间：'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(datajson['time']))
    go.send(meta_data, data)

def start(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    setting = CheckAndGetSettings(meta_data)
    if setting == 404:
        return
    
    dataa = requests.get(url='{0}/api/protected_instance/open?uuid={1}&remote_uuid={2}&apikey={3}'.format(setting.get('MCSMApi'), setting.get('MCSMUuid'), setting.get('MCSMRemote'), setting.get('MCSMKey')))
    datajson = dataa.json()
    
    if datajson['status'] == 200:
        data = '[CQ:face,id=161] 执行成功！\n执行的实例：'+datajson['data']['instanceUuid']+'\n执行时间：'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(datajson['time']))
    else:
        data = '[CQ:face,id=151] 执行失败！\n原因：'+datajson.get('data')+'\n执行时间：'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(datajson['time']))
    go.send(meta_data, data)


def overview(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    setting = CheckAndGetSettings(meta_data)
    if setting == 404:
        return
    
    dataa = requests.get(url='{0}/api/overview?apikey={1}'.format(setting.get('MCSMApi'), setting.get('MCSMKey')))
    datajson = dataa.json()
    if datajson.get('status') == 200:
        data = '[CQ:face,id=161] 面板状态：正常\n[CQ:face,id=161] 面板版本：'+datajson.get('data').get('version')+'\n[CQ:face,id=161] cpu使用率：'+str(datajson.get('data').get('process').get('cpu'))+'\n[CQ:face,id=161] 内存使用率：'+str(hum_convert(datajson.get('data').get('process').get('memory')))+'\n[CQ:face,id=161] 面板登陆次数：'+str(datajson.get('data').get('record').get('logined'))+'\n[CQ:face,id=161] 面板登陆失败次数：'+str(datajson.get('data').get('record').get('loginFailed'))+'\n[CQ:face,id=161] ban ip次数：'+str(datajson.get('data').get('record').get('banips'))+'\n[CQ:face,id=161] 当前系统时间：'+str(datajson.get('data').get('system').get('time'))+'\n[CQ:face,id=161] 系统总共内存：'+str(hum_convert(datajson.get('data').get('system').get('totalmem')))+'\n[CQ:face,id=161] 系统剩余内存：'+str(hum_convert(datajson.get('data').get('system').get('freemem')))+'\n[CQ:face,id=161] 系统类型：'+str(datajson.get('data').get('system').get('type'))+'\n[CQ:face,id=161] 主机名：'+str(datajson.get('data').get('system').get('hostname'))
    else:
        data = '[CQ:face,id=151] 面板状态异常，请联系管理检查面板！'
    
    go.send(meta_data, data)
    

def command(meta_data, iff='true'):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message1 = meta_data.get('message')
    setting = CheckAndGetSettings(meta_data)
    if setting == 404:
        return
    
    dataa = requests.get(url='{0}/api/protected_instance/command?uuid={1}&remote_uuid={2}&apikey={3}&command={4}'.format(setting.get('MCSMApi'), setting.get('MCSMUuid'), setting.get('MCSMRemote'), setting.get('MCSMKey'), message1))
    datajson = dataa.json()
    if datajson['status'] == 200:
        data = '[CQ:face,id=161] 执行成功！\n执行的实例：'+datajson['data']['instanceUuid']+'\n执行时间：'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(datajson['time']))
    else:
        data = '[CQ:face,id=151] 执行失败！\n原因：'+datajson.get('data')+'\n执行时间：'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(datajson['time']))
    if iff == 'true':
        go.send(meta_data, data)

def MCSMAddUser(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    setting = CheckAndGetSettings(meta_data)
    if setting == 404:
        return
    
    dataa = requests.get(url='{0}/api/instance?uuid={1}&remote_uuid={2}&apikey={3}'.format(setting.get('MCSMApi'), setting.get('MCSMUuid'), setting.get('MCSMRemote'), setting.get('MCSMKey')))
    datajson = dataa.json()
    
def MakeMCSh(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    setting = CheckAndGetSettings(meta_data)
    if setting == 404:
        return
    
    dataa = requests.get(url='{0}/api/instance?uuid={1}&remote_uuid={2}&apikey={3}'.format(setting.get('MCSMApi'), setting.get('MCSMUuid'), setting.get('MCSMRemote'), setting.get('MCSMKey')))
    datajson = dataa.json()
    cwd = datajson.get('data').get('config').get('cwd')
    shContent = go.openFile('./plugins/mcserver/start.sh')
    shContent = shContent.replace('{0}', cwd).replace('{1}', setting.get('MCSMUuid'))
    filenamesh = '{0}.sh'.format(time.time())
    filename = '/www/wwwroot/xzydwz/qqbot/createimg/{0}'.format(filenamesh)
    f = open(filename, 'w')
    f.write(shContent)
    f.close()
    
    pams = {
        'group_id': gid,
        'file': filename,
        'name': filenamesh
    }
    data = requests.post(url=meta_data.get('botSettings').get('httpurl')+'/upload_group_file', data=pams)
    if data.json().get('status') == 'failed':
        print(data.json().get('status'))
        go.send(meta_data, '[CQ:face,id=161] 文件发送失败！\n请手动前往 https://xzy.xzy.center/qqbot/createimg/{0} 下载'.format(filenamesh))
    go.send(meta_data, '请将该sh文件上传到服务器然后使用“./{0}”运行即可！'.format(filenamesh))