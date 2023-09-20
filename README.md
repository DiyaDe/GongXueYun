# GongXueYun 自动打卡

这是一个用于自动进行工学云打卡的项目。

# 环境配置

为了成功运行该项目，您需要在您的环境中配置以下内容：

- Python 3.x：项目使用 Python 编写，请确保安装了 Python 3.x 版本。
  - 安装方法：[Python 官方网站](https://www.python.org/downloads/)

- Python 库：您需要安装以下 Python 库。您可以使用 pip 来安装它们：

  ```bash
  pip install requests
  pip install aes_pkcs5
  pip install other_dependency

# 用法
在项目的根目录下执行以下命令以运行项目：
    ```
    python main.py
    ```
# 配置文件文档

以下表格描述了配置文件中的各个字段及其预期值：

| 字段                   | 描述                                       | 示例                               |
|------------------------|------------------------------------------|------------------------------------|
| phone                  | 账号手机号                                | `"phone": "1234567890"`            |
| password               | 账号密码                                   | `"password": "your_password_here"` |
| address                | 详细地址格式                                | `"address": "xx省 · xx市 · xx区 · 在xx"` |
| province               | 省份                                      | `"province": "xx省"`              |
| city                   | 城市                                      | `"city": "xx市"`                  |
| area                   | 区域                                      | `"area": "xx区"`                  |
| latitude               | 经度                                      | `"latitude": "xx.xxxxxx"`         |
| longitude              | 纬度                                      | `"longitude": "yy.yyyyyy"`        |
| bujiao                 | 是否开启补交日报选项                             | `"true"`, `"false"`               |
| bujiao_start_date      | 补交日报的开始日期                              | `"bujiao_start_date": "2023-7-01"`|
| bujiao_end_date        | 补交日报的结束日期                              | `"bujiao_end_date": "2023-7-31"`  |
| reedy                  | 是否开启补交周报选项                             | `"true"`, `"false"`               |
| requirement_week_num   | 补交周报的周数                               | `"requirement_week_num": "5"`     |

## 借鉴的项目

本项目参考或借鉴了以下项目：

- [gonxueyun](https://github.com/github123666/gonxueyun) by [github123666](https://github.com/github123666)
- [Auto-GongXueYun](https://gitee.com/XuanRanDev/Auto-GongXueYun) by XuanRanDev

感谢这些项目的作者对开源社区的贡献。

## 协议

本项目采用 [GNU General Public License v2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) 和 [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 双重许可。
