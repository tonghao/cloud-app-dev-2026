"""
云书签的验证规则（第6讲　第三段）

服务端验证是数据进入系统前的最后一道防线。验证写成独立的函数：
逐条检查，返回错误列表（空列表表示通过），一次报全，用户一次改完。
净化（strip）在视图函数取值时做，这里只检查。
规则与教材配套代码 v2 一致；提示里的「URL」改称「网址」，与添加页上的字一致。
"""

MAX_TITLE_LENGTH = 100
MAX_URL_LENGTH = 500


def validate_bookmark(title, url):
    """验证书签数据，返回错误消息列表"""
    errors = []
    if not title:
        errors.append('标题不能为空')
    elif len(title) > MAX_TITLE_LENGTH:
        errors.append(f'标题不能超过{MAX_TITLE_LENGTH}个字符')
    if not url:
        errors.append('网址不能为空')
    elif not url.startswith(('http://', 'https://')):
        errors.append('网址必须以 http:// 或 https:// 开头')
    elif len(url) > MAX_URL_LENGTH:
        errors.append(f'网址不能超过{MAX_URL_LENGTH}个字符')
    return errors
