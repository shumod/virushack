import tornado.web
import tornado.ioloop
import sys
import os
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(f"Served from {os.getpid()}")

if __name__ == '__main__':

    app = tornado.web.Application([
        (r"/basic", basicRequestHandler)
    ])

    port = 8888
    if(sys.argv.__len__() > 1):
        port = sys.argv[1]

    app.listen(port, 'localhost')
    print(f"Application is ready and listening on port {port}")
    tornado.ioloop.IOLoop.current().start()