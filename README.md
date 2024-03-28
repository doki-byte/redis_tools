# Redis_tools

redis未授权快速写入公钥小工具

一键批量写入公钥，因为nc反弹shell不支持多个，这里就不写多线程利用了

这里如果提示写入成功，但是连接的时间还是需要密码，大概率是权限设置，本地目录的权限，对方服务器对于ssh文件的权限设置等，这些都有要求的

# 使用方法  

```bash
python3 RedisShell.py -t threads -u urls.txt
```
![image](https://github.com/Muhansrc/redis_tools/assets/128204479/4f19cab5-d340-47a6-bc18-132a61fb7697)

# 演示

单个效果演示：

![image](https://github.com/Muhansrc/redis_tools/assets/128204479/5b804cb6-d68e-4c45-b2c7-1cde3109e8c8)


批量测试演示：

![image](https://github.com/Muhansrc/redis_tools/assets/128204479/88e59ff3-166d-4cd5-a5bd-1df62b0eee58)


