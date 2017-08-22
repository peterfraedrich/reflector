from datetime import datetime
from time import sleep
import json
import requests
from threading import Thread
from klein import Klein

class Reflector:
    '''
    main class that does all the work
    '''
    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.http_server = Klein()
        self.handler_threads = []
        self.server_threads = []
        self._log('Instantiated class Reflector', 'info')

        # simple healthcheck URI to check if the app is up
        @self.http_server.route('/__hc', methods=['GET'])
        def healthcheck(request):
            return str(200)

        @self.http_server.route('/')
        @self.http_server.route('/<uri>')
        def handle_get(request):
            '''
            handle incoming requests
            '''
            tpool = []
            for s in range(0,len(self.config['upstream'])):
                tpool.append(self._spawn(target=self._http_redirect, req=request, thread_list=self.handler_threads, index=s))
            for t in tpool:
                t.join()
            return str(request.content.read())

        

    # private methods
    def _log(self, msg, level='info'):
        '''
        logging function, writes to stdout
        '''
        out = {
            'timestamp': str(datetime.now()),
            'level': level.upper(),
            'message': str(msg)
        }
        if self.args.debug:
            print json.dumps(out)

    def _spawn(self, **kwargs):
        '''
        spawn threads
        '''
        if 'req' in kwargs:
            t = Thread(target=kwargs['target'], args=(kwargs['index'], kwargs['req']))
        else:
            t = Thread(target=kwargs['target'])
        t.start()
        return t

    def _http_redirect(self, index, req):
        '''forward http to upstream'''
        if '?' in req.uri:
            params == True
            params = req.uri.split('?')[1]
        else:
            params = ''
        if self.config['upstream'][index]['uri']:
            if params == True:
                url = 'http://{}:{}{}?{}'.format(
                                    self.config['upstream'][index]['host'],
                                    self.config['upstream'][index]['port'],
                                    self.config['upstream'][index]['uri'] + req.uri,
                                    params
                                )
            else:
                url = 'http://{}:{}{}'.format(
                                    self.config['upstream'][index]['host'],
                                    self.config['upstream'][index]['port'],
                                    self.config['upstream'][index]['uri'] + req.uri
                                )
        else:
            url = 'http://{}:{}{}'.format(
                                self.config['upstream'][index]['host'],
                                self.config['upstream'][index]['port'],
                                req.uri
                            )
        headers = req.getAllHeaders()
        body = req.content
        if req.method.lower() in ['get', 'options']:
            r = requests.get(url, headers=headers, timeout=5)
        elif req.method.lower() in ['post', 'put', 'delete']:
            r = requests.post(url, headers=headers, data=body, timeout=5)



    # public methods
    def start(self):
        '''
        start listening for connections
        '''
        self._log('Starting Reflector')
        self.http_server.run(self.args.host, self.args.port)
        return



    