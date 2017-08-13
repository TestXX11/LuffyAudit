# 堡垒机数据库

![设计表结构](http://onk83djzp.bkt.clouddn.com/15022795700751.jpg)

## IDC
>机房表
- name 

## Host
>主机表,存储所有的主机信息:主机名,ip 地址,端口,机房,是否启用

## HostGroup
>主机组
- 组名
- 那个用户对这个组有控制权限


## HostUser
>存储主机 ssh 登录信息
- auth_type_choices (ssh 连接类型枚举字段)
- auth_type(连接类型)
- username(用户名)
- password(用户密码)

## HostUserBind
>绑定主机和用户,每个主机地址和ssh用户/密码是唯一的,
- host(主机,FK)
- host_user(对应的主机登录密码)
- 唯一标识

```python
class Meta:
   unique_together = ('host', 'host_user')
```

## AuditLog
> 审计日志,用来记录操作

## Account
>堡垒机用户
- user(对应的django admin 的用户)
- name (昵称)
- host_user_binds(用户对那个主机有权限)
- host_groups 对哪个主机组有控制权限

![](http://onk83djzp.bkt.clouddn.com/15022807426251.jpg)


