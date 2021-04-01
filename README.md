# Band-Width-limit

此脚本可用于对linux设备进行对自身网络带宽添加限制，一般用于各类场景的测试实验，或者对集群部署进行资源调配。

## 使用

```
sudo python3 BW_limit.py -b 60 -f build   # 对设备限制为60 Mbit/sec 带宽

sudo python3 BW_limit.py -f del           # 释放先前的带宽限制
```

