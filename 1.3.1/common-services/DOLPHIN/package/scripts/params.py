# -*- coding: utf-8 -*-
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import sys
from resource_management import *
from resource_management.core.logger import Logger
from resource_management.libraries.functions import default
import commands
from resource_management.libraries.script.script import Script
reload(sys)
sys.setdefaultencoding('utf-8')


config = Script.get_config()

#hdp info
cmd = "/usr/bin/hdp-select versions"
hdp_version = commands.getoutput(cmd)
hdp_base_dir = '/usr/hdp/' + hdp_version

#log config content
worker_logback = config['configurations']['dolphin-logback']['worker_logback.xml']
master_logback = config['configurations']['dolphin-logback']['master_logback.xml']
apiserver_logback = config['configurations']['dolphin-logback']['apiserver_logback.xml']
alert_logback = config['configurations']['dolphin-logback']['alert_logback.xml']

print config['configurations']['dolphin-logback']

# package download url
download_url = config['configurations']['dolphin-ambari-config']['dolphinscheduler.package.download.url']
jdbc_driver_download_url = config['configurations']['dolphin-ambari-config']['jdbc.connector.download.url']


# conf_dir = "/etc/"
dolphin_home =hdp_base_dir + "/dolphinscheduler"
dolphin_conf_dir = dolphin_home + "/conf"
dolphin_log_dir = "/var/log/dolphinscheduler"
dolphin_bin_dir = dolphin_home + "/bin"
dolphin_lib_jars = dolphin_home + "/lib/*"
dolphin_pidfile_dir = "/var/run/dolphinscheduler"

rmHosts = default("/clusterHostInfo/rm_host", [])

# dolphin-env
dolphin_env_map = {}
dolphin_env_map.update(config['configurations']['dolphin-env'])
Logger.info("Load dolphin_env_map config: %s" % dolphin_env_map)

# which user to install and admin dolphin scheduler
dolphin_user = dolphin_env_map['dolphin.user']
dolphin_group = dolphin_env_map['dolphin.group']

# .dolphinscheduler_env.sh
dolphin_env_path = dolphin_conf_dir + '/env/dolphinscheduler_env.sh'
dolphin_env_content = dolphin_env_map['dolphinscheduler-env-content']

# database config
dolphin_database_config = {}
dolphin_database_config['dolphin_database_type'] = dolphin_env_map['dolphin.database.type']
dolphin_database_config['dolphin_database_host'] = dolphin_env_map['dolphin.database.host']
dolphin_database_config['dolphin_database_port'] = dolphin_env_map['dolphin.database.port']
dolphin_database_config['dolphin_database_username'] = dolphin_env_map['dolphin.database.username']
dolphin_database_config['dolphin_database_password'] = dolphin_env_map['dolphin.database.password']

if 'mysql' == dolphin_database_config['dolphin_database_type']:
    dolphin_database_config['dolphin_database_driver'] = 'com.mysql.jdbc.Driver'
    dolphin_database_config['driverDelegateClass'] = 'org.quartz.impl.jdbcjobstore.StdJDBCDelegate'
    dolphin_database_config['dolphin_database_url'] = 'jdbc:mysql://' + dolphin_env_map['dolphin.database.host'] \
                                                      + ':' + dolphin_env_map['dolphin.database.port'] \
                                                      + '/dolphinscheduler?useUnicode=true&characterEncoding=UTF-8'
else:
    dolphin_database_config['dolphin_database_driver'] = 'org.postgresql.Driver'
    dolphin_database_config['driverDelegateClass'] = 'org.quartz.impl.jdbcjobstore.PostgreSQLDelegate'
    dolphin_database_config['dolphin_database_url'] = 'jdbc:postgresql://' + dolphin_env_map['dolphin.database.host'] \
                                                      + ':' + dolphin_env_map['dolphin.database.port'] \
                                                      + '/dolphinscheduler'


# datasource.properties
dolphin_database_map = {}
dolphin_database_map['spring.datasource.driver-class-name'] = dolphin_database_config['dolphin_database_driver']
dolphin_database_map['spring.datasource.url'] = dolphin_database_config['dolphin_database_url']
dolphin_database_map['spring.datasource.username'] = dolphin_database_config['dolphin_database_username']
dolphin_database_map['spring.datasource.password'] = dolphin_database_config['dolphin_database_password']

# application-alert.properties
dolphin_alert_map = {}
wechat_push_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$token'
wechat_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$corpId&corpsecret=$secret'
wechat_team_send_msg = '{\"toparty\":\"$toParty\",\"agentid\":\"$agentId\",\"msgtype\":\"text\",\"text\":{\"content\":\"$msg\"},\"safe\":\"0\"}'
wechat_user_send_msg = '{\"touser\":\"$toUser\",\"agentid\":\"$agentId\",\"msgtype\":\"markdown\",\"markdown\":{\"content\":\"$msg\"}}'

dolphin_alert_map['enterprise.wechat.push.ur'] = wechat_push_url
dolphin_alert_map['enterprise.wechat.token.url'] = wechat_token_url
dolphin_alert_map['enterprise.wechat.team.send.msg'] = wechat_team_send_msg
dolphin_alert_map['enterprise.wechat.user.send.msg'] = wechat_user_send_msg
dolphin_alert_map.update(config['configurations']['dolphin-alert'])

# application-api.properties
dolphin_app_api_map = {}
dolphin_app_api_map['logging.config'] = 'classpath:apiserver_logback.xml'
dolphin_app_api_map['spring.messages.basename'] = 'i18n/messages'
dolphin_app_api_map['server.servlet.context-path'] = '/dolphinscheduler/'
dolphin_app_api_map.update(config['configurations']['dolphin-application-api'])
dolphin_app_api_map['spring.servlet.multipart.max-file-size'] = dolphin_app_api_map['spring.servlet.multipart.max-file-size'] + "MB"
dolphin_app_api_map['spring.servlet.multipart.max-request-size'] = dolphin_app_api_map['spring.servlet.multipart.max-request-size'] + "MB"

# application-dao.properties
dolphin_application_map = {}
dolphin_application_map['spring.datasource.type'] = 'com.alibaba.druid.pool.DruidDataSource'
dolphin_application_map['spring.datasource.driver-class-name'] = dolphin_database_config['dolphin_database_driver']
dolphin_application_map['spring.datasource.url'] = dolphin_database_config['dolphin_database_url']
dolphin_application_map['spring.datasource.username'] = dolphin_database_config['dolphin_database_username']
dolphin_application_map['spring.datasource.password'] = dolphin_database_config['dolphin_database_password']
dolphin_application_map.update(config['configurations']['dolphin-application'])

# common.properties
dolphin_common_map = {}

if 'yarn-site' in config['configurations'] and \
        'yarn.resourcemanager.webapp.address' in config['configurations']['yarn-site']:
    yarn_resourcemanager_webapp_address = config['configurations']['yarn-site']['yarn.resourcemanager.webapp.address']
    yarn_application_status_address = 'http://' + yarn_resourcemanager_webapp_address + '/ws/v1/cluster/apps/%s'
    dolphin_common_map['yarn.application.status.address'] = yarn_application_status_address

rmHosts = default("/clusterHostInfo/rm_host", [])
if len(rmHosts) > 1:
    dolphin_common_map['yarn.resourcemanager.ha.rm.ids'] = ','.join(rmHosts)
else:
    dolphin_common_map['yarn.resourcemanager.ha.rm.ids'] = ''

dolphin_common_map_tmp = config['configurations']['dolphin-common']

Logger.info("Load dolphin-common config: %s" % dolphin_common_map_tmp)

data_basedir_path = dolphin_common_map_tmp['data.basedir.path']
process_exec_basepath = data_basedir_path + '/exec'
data_download_basedir_path = data_basedir_path + '/download'
dolphin_common_map['process.exec.basepath'] = process_exec_basepath
dolphin_common_map['data.download.basedir.path'] = data_download_basedir_path
dolphin_common_map['dolphinscheduler.env.path'] = dolphin_env_path

dolphin_app_api_map['resource.storage.type'] = dolphin_common_map_tmp['resource.storage.type']
dolphin_common_map['resource.storage.type'] = dolphin_common_map_tmp['resource.storage.type']

zookeeperHosts = default("/clusterHostInfo/zookeeper_server_hosts", [])
if len(zookeeperHosts) > 0 and "clientPort" in config['configurations']['zoo.cfg']:
    clientPort = config['configurations']['zoo.cfg']['clientPort']
    zookeeperPort = ":" + clientPort + ","
    dolphin_common_map['zookeeper.quorum'] = zookeeperPort.join(zookeeperHosts) + ":" + clientPort

dolphin_common_map.update(config['configurations']['dolphin-common'])

# quartz.properties
dolphin_quartz_map = {}
dolphin_quartz_map['org.quartz.jobStore.driverDelegateClass'] = dolphin_database_config['driverDelegateClass']
dolphin_quartz_map['org.quartz.dataSource.myDs.driver'] = dolphin_database_config['dolphin_database_driver']
dolphin_quartz_map['org.quartz.dataSource.myDs.URL'] = dolphin_database_config['dolphin_database_url']
dolphin_quartz_map['org.quartz.dataSource.myDs.user'] = dolphin_database_config['dolphin_database_username']
dolphin_quartz_map['org.quartz.dataSource.myDs.password'] = dolphin_database_config['dolphin_database_password']
dolphin_quartz_map.update(config['configurations']['dolphin-quartz'])

# zookeeper properties
dolphin_zookeeper_map = {}
dolphin_zookeeper_map['zookeeper.quorum'] = dolphin_common_map['zookeeper.quorum']
dolphin_quartz_map.update(config['configurations']['dolphin-zookeeper'])

# if 'ganglia_server_host' in config['clusterHostInfo'] and \
#         len(config['clusterHostInfo']['ganglia_server_host'])>0:
#   ganglia_installed = True
#   ganglia_server = config['clusterHostInfo']['ganglia_server_host'][0]
#   ganglia_report_interval = 60
# else:
#   ganglia_installed = False
