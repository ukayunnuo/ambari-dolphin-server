# Ambari2.7版本集成Dolphinscheduler1.3.1

## 1. 下载包

### Dolphinscheduler 安装包下载

[apache-dolphinscheduler-incubating-1.3.1-dolphinscheduler-bin.tar.gz](https://archive.apache.org/dist/incubator/dolphinscheduler/1.3.1/apache-dolphinscheduler-incubating-1.3.1-dolphinscheduler-bin.tar.gz)

安装包目录如下：

![img.png](images%2Fimg.png)

### java-mysql-connector依赖包下载

[mysql-connector-java-5.1.49.jar](https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.49/mysql-connector-java-5.1.49.jar)

## 2. 配置 mysql数据库

### 创建数据库和用户

```sql
CREATE DATABASE dolphinscheduler CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'dolphinscheduler'@'%' IDENTIFIED BY 'dolphinscheduler';
GRANT ALL PRIVILEGES ON dolphinscheduler.* TO 'dolphinscheduler'@'%';
FLUSH PRIVILEGES;
```

### 执行安装包的sql文件进行对表的创建

sql文件位置：`apache-dolphinscheduler-incubating-1.3.1-dolphinscheduler-bin.tar.gz` 解压后的 sql文件夹下的
`dolphinscheduler_mysql.sql`
![img1.png](images%2Fimg1.png)

![img_1.png](images%2Fimg_1.png)

## 3. 安装jdk1.8环境

需要在选择部署的主机上安装jdk1.8环境。

```bash
# 安装jdk1.8环境(已有jdk版本跳过此步骤)
yum install -y java-1.8.0-openjdk-devel
```

dolphinscheduler的部署脚本中会获取`JAVA_HOME` 环境变量，所以需要设置`JAVA_HOME`环境变量。

编辑`/etc/profile`文件

```bash
vim /etc/profile
```

添加以下内容：

```bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
```

更新`/etc/profile`文件

```bash
source /etc/profile
```

![img3.png](images%2Fimg3.png)

## 4. 将安装包和依赖包放置在 apache 的 httdp 服务上

放置路径：

```bash
/var/www/html/DOLPHIN
```

![img4.png](images%2Fimg4.png)

浏览器访问：

![img5.png](images%2Fimg5.png)

## 5. 放置ambari-dolphin-server插件脚本

### metainfo.xml 文件

将本项目中的`1.3.1/statcks/DOLPHIN/metainfo.xml` 放置在`/var/lib/ambari-server/resources/stacks/HDP/3.1/services/DOLPHIN/metainfo.xml`目录下。

![img.png](img.png)

### 部署脚本文件

将本项目中的`1.3.1/common-services/DOLPHIN` 文件夹放置在`/var/lib/ambari-server/resources/common-services/DOLPHIN/1.3.1` 目录下。

![img_3.png](images%2Fimg_3.png)

## 6. 重启ambari-server

```bash
ambari-server restart
```

## 7. 添加 Dolphin Scheduler 服务

### 在添加服务页面上会出现Dolphin Scheduler服务

![img_4.png](images%2Fimg_4.png)

### 选择安装主机节点

![img_5.png](images%2Fimg_5.png)

![img_6.png](images%2Fimg_6.png)

### 配置信息

![img_7.png](images%2Fimg_7.png)

高级配置需要配置下载的安装包和mysql依赖包路径：

![img_8.png](images%2Fimg_8.png)

官网中的logback配置有问题，打开是空的，本项目已经进行修复，各位也可以检查一下，如果版本问题也没有正常解析到日志配置，可以手动进行复制上去。

![img_9.png](images%2Fimg_9.png)

各服务的logback配置文件：

文件路径： 安装包的 conf 文件夹下

![img_10.png](images%2Fimg_10.png)

### 查看安装信息

![img_13.png](images%2Fimg_13.png)

### 安装成功

**dolphin scheduler默认账号密码：admin/dolphinscheduler123**

点击服务的超链接进行快速跳转：

![img_11.png](images%2Fimg_11.png)

进入首页：

![img_12.png](images%2Fimg_12.png)