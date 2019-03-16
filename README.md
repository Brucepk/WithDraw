# Python骚操作 | 还原已撤回的微信消息

### 本代码文章首发于公众号「Python知识圈」，如需转载，请通过公众号联系作者pk哥，谢谢

![公众号](https://github.com/Brucepk/pk.github.io/blob/master/gzh.jpg)

#### 公众号里提供了我的微信，可以联系到我。

一大早醒来，发现女神昨晚发来三条消息，但是显示都已撤回，OMG，我错过了什么？群里有一个漂亮妹纸的爆照照片撤回了，想看又看不到！群里大佬分享的经典语录被撤回了，感觉错过一个亿！怎么办？用无所不能的 Python 就可以将这些撤回的消息发给你的微信，让你从此走上人生巅峰

#### 项目环境
语言：Python3
编辑器：Pycharm

#### 导包
itchat：控制微信的第三方库

这个库相信大家不陌生了，之前写的 Python 机器人陪你聊天   Python 定时给女神发早安 两篇文章里用的 wxpy 库就是在 itchat 库的基础上封装的。

#### 效果展示
以下截图显示的撤回消息类型依次是文字消息、微信自带表情、图片、语音、定位地图、名片、公众号文章、音乐、视频。有群里撤回的，也有个人号撤回的。
![撤回1](https://github.com/Brucepk/pk.github.io/blob/master/%E6%92%A4%E5%9B%9E1.jpg)
![撤回2](https://github.com/Brucepk/pk.github.io/blob/master/%E6%92%A4%E5%9B%9E2.jpg)



# 文章详细解析[点击这里查看](https://mp.weixin.qq.com/s?__biz=MzU4NjUxMDk5Mg==&mid=2247484157&idx=1&sn=e0ceb2096458774988026d7dbb441b78&scene=19#wechat_redirect)
