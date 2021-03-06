import requests

from testhttpserver import Server
import testhttpserver
import testhttpserver.server as mod

class DescribePackage(object):

    def should_have_version_number(self):
        assert testhttpserver.__version__ == '0.1.2'

class BaseHTTPServerTest(object):

    @classmethod
    def setup_class(cls, *args, **kwargs):
        cls.server = Server(*args, **kwargs)

    @classmethod
    def teardown_class(cls):
        cls.server.join()

class DescribeGettingData(BaseHTTPServerTest):

    @classmethod
    def setup_class(cls, port=8010, response_status=200):
        BaseHTTPServerTest.setup_class(port, response_content='CONTENT')

        cls.response = requests.get('http://localhost:8010/')

    def should_return_content(self):
        assert self.response.content == 'CONTENT'

    def should_respond_with_status_200(self):
        assert self.response.status_code == 200

    def should_save_request_path(self):
        assert self.server.request_path == '/'


class DescribePostingData(BaseHTTPServerTest):

    @classmethod
    def setup_class(cls, port=8020):
        BaseHTTPServerTest.setup_class(
            port,
            response_status=201,
            response_headers=[('Another-Header', 'AWESOME!')]
        )
        cls.response = requests.post(
            'http://localhost:8020/path',
            data='POST DATA',
            headers={'Custom-Header': 'Custom-Header-Value'}
        )

    def should_save_post_content(self):
        assert self.server.request_content == 'POST DATA'

    def should_return_correct_status_code(self):
        assert self.response.status_code == 201

    def should_save_headers(self):
        assert self.server.request_headers['Custom-Header'] == 'Custom-Header-Value'

    def should_save_request_path(self):
        assert self.server.request_path == '/path'

    def should_respond_with_customer_headers(self):
        assert self.response.headers['Another-Header'] == 'AWESOME!'


class DescribeServer(object):

    def should_allow_recreating_server_on_same_port(self):
        for i in range(2):
            server = Server(port=8000, response_status=200,
                            response_content='')
            requests.post('http://localhost:8000/')
            server.join()
