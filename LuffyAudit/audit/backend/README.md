# 用户登录堡垒机认证,和登录后的 shell
- UserShell(类)
    - auth(认证逻辑)
    - start(交互程序)

## auth方法

```python
# django 登录组件
from django.contrib.auth import authenticate

def auth(self):
    '''
    username,password 返回登录结果
    :return:
    '''
    count = 0
    while count < 3:
        username = input("username:").strip()
        password = input("password:").strip()
        # Django 使用自带登录认证
        user = authenticate(username=username, password=password)
        # None 代表认证不成功
        # user object ，认证对象 ,user.name
        if not user:
            count += 1          # 登录计数
            print("Invalid username or password!")
        else:
            self.user = user            # 登录成功  user 是一个对象
            return True                 # 必须返回 True
    else:
        print("too many attempts.")     # 错误次数过多
```

## start方法
>交互逻辑,如果某些主机没有分组,把他们放到未分组的下面
1. 列出当前用户所控制的所有主机组和某些单独控制的主机
2. 用户进行选择某组,列出当前组下的主机(可以不是全部)
3. 用户选择某台主机后,进行交互的逻辑

``` python
# 获取当前用户的所控制的主机组
host_groups = self.user.account.host_groups.all()

# 循环主机组,打印出索引,组名,主机数
for index, group in enumerate(host_groups):
    print("%s.\t%s[%s]" % (index, group, group.host_user_binds.count()))

# 未分组的机器,主机数
print("%s.\t未分组机器[%s]" % (len(host_groups), self.user.account.host_user_binds.count()))
```