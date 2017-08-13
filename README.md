# 知识点:
- [堡垒机表结构](https://github.com/317828332/LuffyAudit/tree/cvno/audit)
- [使用Django登录组件登录](https://github.com/317828332/LuffyAudit/tree/cvno/audit/backend)



## `audit_shell.py` shell 交互
>Django 登录组件启动程序

```python
# 导入登录逻辑代码文件
from audit.backend import user_interactive

# 设置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
    django.setup() # 手动注册django所有的APP

    obj = user_interactive.UserShell(sys.argv)
    obj.start()     # 认证逻辑
```


# 为什么要开发堡垒机?
>安全!

# 堡垒机架构
![](http://onk83djzp.bkt.clouddn.com/15022796285217.jpg)

堡垒机部署上后，同时要确保你的网络达到以下条件：

- 所有人包括运维、开发等任何需要访问业务系统的人员，只能通过堡垒机访问业务系统
    * 回收所有对业务系统的访问权限，做到除了堡垒机管理人员，没有人知道业务系统任何机器的登录密码
    * 网络上限制所有人员只能通过堡垒机的跳转才能访问业务系统 
- 确保除了堡垒机管理员之外，所有其它人对堡垒机本身无任何操作权限，只有一个登录跳转功能
- 确保用户的操作纪录不能被用户自己以任何方式获取到并篡改 


# 堡垒机功能实现需求
## 业务需求
1. 兼顾业务安全目标与用户体验，堡垒机部署后，不应使用户访问业务系统的访问变的复杂，否则工作将很难推进，因为没人喜欢改变现状，尤其是改变后生活变得更艰难
2. 保证堡垒机稳定安全运行， 没有100%的把握，不要上线任何新系统，即使有100%把握，也要做好最坏的打算，想好故障预案

## 功能需求
- 所有的用户操作日志要保留在数据库中
- 每个用户登录堡垒机后，只需要选择具体要访问的设置，就连接上了，不需要再输入目标机器的访问密码
- 允许用户对不同的目标设备有不同的访问权限，例:
    * 对10.0.2.34 有mysql 用户的权限
    * 对192.168.3.22 有root用户的权限
    * 对172.33.24.55 没任何权限
- 分组管理，即可以对设置进行分组，允许用户访问某组机器，但对组里的不同机器依然有不同的访问权限　


# 审计系统/堡垒机
主机管理

堡垒机记录用户操作方式
1. 更改 ssh客户端的源代码,10W+
2. 修改已有 python ssh 库,加入指令记录的功能

# 开发流程
1. 需求分析
2. 原型设计
3. 设计表结构
4. 架构设计
5. 开发

**Django :the framework for perfectionist with deadlines!**


