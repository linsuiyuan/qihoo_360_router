"""一些帮助函数"""
import datetime
import functools

from Crypto.Cipher import AES  # noqa
from Crypto.Util.Padding import pad, unpad  # noqa
from binascii import unhexlify, hexlify


def qihoo_aes_encrypt(rand_key_hex, text):
    """AES加密"""
    # 将十六进制字符串转换为字节
    rand_key = unhexlify(rand_key_hex)
    # 将IV转换为字节
    iv = b"360luyou@install"  # Latin1编码的字符串

    # 创建AES加密对象
    cipher = AES.new(rand_key, AES.MODE_CBC, iv)

    # 对明文进行填充
    padded_plaintext = pad(text.encode('utf-8'), AES.block_size)

    # 执行加密
    ciphertext = cipher.encrypt(padded_plaintext)

    return hexlify(ciphertext).decode()


def qihoo_aes_decrypt(rand_key_hex, ciphertext_hex):
    """AES解密"""
    # 将十六进制字符串转换为字节
    rand_key = unhexlify(rand_key_hex)
    # 将IV转换为字节
    iv = b"360luyou@install"  # Latin1编码的字符串

    # 创建AES解密对象
    cipher = AES.new(rand_key, AES.MODE_CBC, iv)

    # 将密文从十六进制转换为字节
    ciphertext = unhexlify(ciphertext_hex)

    # 执行解密
    padded_plaintext = cipher.decrypt(ciphertext)

    # 去填充
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext.decode('utf-8')


def qihoo_password_encrypt(key_obj, password):
    """360路由密码加密"""
    password = qihoo_aes_decrypt(password[:32], password[32:])
    encrypt_pass = qihoo_aes_encrypt(rand_key_hex=key_obj['rand_key'],
                                     text=password)
    pass_ = key_obj['key_index'] + encrypt_pass
    return pass_


def is_in_time_period(*time_period: str, time_=None):
    """
    判断是否在某些时间断内
    :param time_period: ['00:00-20:00', '21:00-23:59'] 或者 '00:00-20:00'
    :param time_: 指定时间（如'20:00'），未指定则默认当前时间
    :return:
    """
    if time_ is None:
        time_ = datetime.datetime.now().strftime('%H:%M')

    for period in time_period:
        start, end = period.split('-')
        if start <= time_ < end:
            return True
    return False


def run_with_semaphore(sem):
    """限制异步并发数量"""
    def decorator(func):  # noqa
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):  # noqa
            async with sem:
                result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator


if __name__ == '__main__':
    rand_key_ = '9ceef3e000584938432a932b7d803c71'
    t = '.'
    res = qihoo_aes_encrypt(rand_key_, t)
    print(res)

    res = qihoo_aes_decrypt(rand_key_, res)
    print(res)
