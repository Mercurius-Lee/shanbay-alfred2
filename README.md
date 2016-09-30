# Shanbay-Alfred2-Workflow

扇贝网Alfred2 workflow，主要用于单词查询、添加单词到词库、发音。


## 安装

下载[`Shanbay.alfredworkflow`](https://github.com/alswl/shanbay-alfred2/raw/master/Shanbay.alfredworkflow)文件

双击文件导入即可。

## 使用

*   授权
    *   任意使用查询功能，如 `sb love` 会检查权限情况，如果权限不存在或过期，会自动进入授权页面
    *   在扇贝官网的授权界面输入帐号密码，然后授权
    *   出现 `Shanbay OAuth2` 之后，将完整的 URL 复制下来，并在 Alfred 里面输入 `sbauth https://api.shanbay.com/oauth2/auth/success/#access_token=xxx&token_type=Bearer&state=&expires_in=2592000&scope=read+write`（后面的 URL请替换为你自己复制的 URL）
    *   授权完成，使用 `sb love` 测试，按回车即可以添加到单词库
*   查单词
    *   使用 `sb love` 查询单词
*   添加到单词库
    *   使用 `sb love` 查询单词，然后使用回车即添加到单词库
*   打开单词
    *   使用 `sb love` 查询单词，按住 `Command` + 回车，打开扇贝官网对应的单词页面
*   听发音
    *   使用 `sb love` 查询单词，按住 `Ctrl` + 回车，即可播放语音


注：授权有效期为一个月，过期需重新授权。


## 其它

感谢原作者 [https://github.com/henter/Shanbay-Alfred2](https://github.com/henter/Shanbay-Alfred2) 开发。

我的改进：

*   不使用 code 授权模式，改为 token 直接授权，不用打开一个第三方网站
*   支持听单词语音
*   移除例句查询功能
