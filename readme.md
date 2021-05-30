# 准备



### 环境安装



- **Python库**

文件夹里面有requirements.txt的文本文件（在cmd运行下面代码安装所需环境，建议在虚拟环境中）

```python
pip install -r requirements.txt
```

如果有出现报错信息，原因一般如下：

- python版本问题（具体解决方法自行百度，我的python版本是3.8）
- 第三方库版本问题（自行安装，然后将requirements.txt中对应的库删除，重新运行）



- **MySQL**（仅用于本地测试）
  - 官网下载，具体配置网上有
  - 安装phpstudy（小皮面板），傻瓜式配置环境



### 文档说明



- **根目录-Test-aitongue_v2_0（测试文件暂不做介绍）**
  - face_img：保存面部图片信息
  - lg_aitongue：逻辑实现文件
    - api_1_0：存放视图（包括初始化文件，登录，体质记录，面诊，量表保存，个人信息保存和个人页面等）
    - __init__.py：项目初始化文件（包括app，db和flask后台）
    - models.py：数据库映射文件
    - response_code.py：全局错误码
  - libs：腾讯云对象存储（暂未使用）
  - log：日志文件
  - migrations：数据库迁移文件（如需重新迁移则需删除）
  - utils：自定义文件
    - ai_tongue：舌诊逻辑（这部分是第一版的改写，因此没有那么规范化，请谅解）
      - upload_picture：用于对用户舌头图片的接收和上传（中间仓库的作用，类似对象存储），如果使用对象存储，在picSegment.py，runModel3.py和tongue_diagnosis.py中修改文件路径，然后删掉该文件夹即可
      - constant.py：常量文件
      - picSegment.py：舌头分割及检测逻辑代码
      - runModel3.py：舌头图像分类模型代码
      - tongue_diagnosis.py：舌诊逻辑文件
    - commons：存放自定义的函数
  - config.py：配置文件（包括mysql配置等）
  - manage.py：主入口文件
  - requirements.txt：Python第三方库版本文件



# 开始

### 运行

- **本地运行**

  - 做数据库迁移

    打开MySQL，新建数据库命名为aitongue，然后在cmd中切换到有manage.py的目录，运行如下命令

    - python manage.py db init
    - python manage.py db migrate
    - python manage.py db upgrade

    当看到aitongue中有wechat_info, user_info, scale_info, mouth_info, face_info, alembic_version这六个表，说明数据库迁移成功

    如果中途报错，一般如下原因：

    1. 没安装pymysql，自行安装即可
    2. migrations已存在，删除然后重新迁移
    3. 其他问题，可以百度

  - 在PyCharm中运行manage.py文件，如果报了类似runserver的错误，则在运行配置中添加runserver


  - 接口测试

    用postman进行接口测试

    教程：https://blog.csdn.net/fxbin123/article/details/80428216

  - 其他

    项目自测没问题，但可能由于环境不一样，因此可能会出现报错，具体自行百度查看

- **服务器运行（Linux）**

  - 安装MySQL（推荐直接使用宝塔面板，这样不用自行安装MySQL，参考后文）

  - 将项目文件打包（xxx.tar.gz格式，工具很多，我用的是7-Zip），上传到服务器中进行解压

    ```Ubuntu
    # 先进入到有压缩包的目录
    tar -zxvf 压缩包
    ```

  - 同样按照本地运行的步骤做数据库迁移，中途可能会报错（access denied for user xxx(using password: YES)），出现该错误可能是用户名和密码不正确，修改config.py文件，将自己的用户名和密码修改一下即可。如果出现其他报错，则自行百度



  - 在服务器运行manage.py

    有两种方式：

    - 直接运行，python manage.py runserver（如果不设置host和port，该项目只能本服务器访问，不能通过外网访问）
    - 部署，部署的方式有很多种，推荐gunicorn部署（后面会提到）

    报错日志的查看可以百度一下，我没有进行查看（个人建议做一下，方便查错）

  - 接口测试

    同样用postman做测试，只不过ip换成服务器的公网ip，或者直接用域名（部署后）

  - 其他

    服务器的运行会有很多不确定因素，但是要相信百度，也要有足够的耐心



### 部署



flask框架在Linux有五大部署方法

推荐两种：

1. gunicorn（个人项目）
2. flask+nginx+gunicorn（大项目）

本项目使用的是flask+nginx+gunicorn的部署方法



**ps：下面这些操作可以使用xshell，也可以使用云服务器的终端系统**

- 域名解析+备案（这里就不再赘述，可以参考购买云服务器的官网文档），备案的时间较长，所以可以先备案

- 安装pip3

```ubuntu
sudo apt install python3-pip
```

- 安装虚拟环境（非必须，如果有多个项目则建议安装虚拟环境）

  - 安装virtualenv

    ```
    pip3 install virtualenv
    ```

  - 安装virtualenvwrapper

    ```
    pip3 install virtualenvwrapper
    ```

  - 设置Linux的环境变量，每次启动就加载virtualenvwrapper

    ```
    打开文件
    vim ~/.bashrc
    写入以下两行代码
    export WORKON_HOME=~/Envs   #设置virtualenv的统一管理目录
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'   #添加virtualenvwrapper的参数，生成干净隔绝的环境
    
    export VIRTUALENVWRAPPER_PYTHON=/opt/python347/bin/python3     #指定python解释器
    source /opt/python34/bin/virtualenvwrapper.sh #执行virtualenvwrapper安装脚本
    读取文件，使得生效，此时已经可以使用virtalenvwrapper
    source ~/.bashrc
    ```

  - 使用virtualenvwrapper

    ```
    # 创建虚拟环境
    mkvirtualenv 虚拟环境名
    
    # 激活虚拟环境
    workon 虚拟环境名
    ```

参考来源：https://www.cnblogs.com/pyyu/p/9015317.html

我遇见的报错：

 	1. virtualenvwrapper could not find virtualenv in your path：参考https://blog.csdn.net/weixin_30905981/article/details/101587671
 	2. virtualenv: error: unrecognized arguments: --no-site-packages：参考https://blog.csdn.net/weixin_46728614/article/details/106779406



- 安装宝塔面板（个人推荐，免去安装nginx和MySQL的麻烦）

直接百度“宝塔”，安装Linux版本，选择对应的服务器的命令进行安装（如果使用宝塔界面，推荐Centos系统）

我的是Ubuntu18.04，则用如下命令

```ubuntu
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
```

其他系统的命令可在官网（https://www.bt.cn/bbs/thread-19376-1-1.html）查看，也可以看下面这张图

![baota](D:\typora\aitongue img\baota.png)

宝塔界面安装完成后，会有nginx和MySQL这两个软件

如果系统是Centos7.x，可以尝试宝塔的Python项目管理器，可以快速部署Python项目，如果不是则自行部署



- 安装gunicorn

```
pip3 install gunicorn
```

安装好后，写一个简单的hello.py进行测试（部署前先进入到有flask实例文件的目录）

```
gunicorn -w 4 -b 0.0.0.0:5000 hello:app
```

-w：进程数，推荐书目：CPU个数*2+1

-b：gunicorn绑定的服务器套接字

-D：后台运行

参考：

常用参数：https://www.jianshu.com/p/8e5b2b995b90

详细参数：https://www.cnblogs.com/zgcblog/p/10923913.html



- nginx配置（在宝塔面板的网站的配置文件中添加配置，因为该文件配置有server_name，因此只需添加如下配置即可）

```nginx
    location /
    {
        proxy_pass http://0.0.0.0:9090;
        proxy_redirect     off;
        proxy_set_header   Host                 $http_host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
    }
```

重载nginx配置，访问服务器ip+配置的端口号（我的是9090），如果可以访问到测试文件hello.py的内容，则说明配置成功



- 配置ssl证书（看官方文档，用宝塔配置）



配置好后，能够使用域名访问，并且能够通过https访问，则说明ssl证书配置成功。这样项目部署大致就完成了。



ps：在此特别致谢Gaozhi Tang，Chufan Jian，Zhenxiong Wu对舌诊模型和接口编写的贡献
