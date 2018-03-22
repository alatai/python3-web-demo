# -- coding:utf-8 --

import asyncio


# 获取网站首页
@asyncio.coroutine
def wget(host):
    print('wget %s ...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
        # Ignore the body, close the socket
        writer.close()
    print('==========================================================')


# 获取EventLoop
loop = asyncio.get_event_loop()
# 设置任务
tasks = [wget(host) for host in ['www.baidu.com', 'www.sina.com', 'www.sohu.com']]
# 执行coroutine
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
