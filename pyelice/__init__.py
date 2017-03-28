import copy
import json
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

DEFAULT_URL = 'https://api-v4.elice.io'
DEFAULT_ORGANIZATION_NAME = 'academy'
DEFAULT_COUNT = 20
DEFAULT_ENCODING = 'utf-8'
DEFAULT_RETRY_DELAY = 5

class EliceResponseError(Exception):
    def __init__(self, result):
        try:
            self.message = result['fail_message']
        except:
            self.message = 'unknown error is received from the server'
        try:
            self.code = result['fail_code']
        except:
            self.code = 'unknown'
        self.body = result

class Elice:
    def __init__(self, url=DEFAULT_URL):
        self.url = self._format_url(url)

    def _format_url(self, url):
        while url.endswith('/'):
            url = url[:-1]
        return url

    def _format_path(self, path):
        if not path.startswith('/'):
            path = '/' + path
        if not path.endswith('/'):
            path = path + '/'
        while path.endswith('//'):
            path = path[:-1]
        return path

    def request(self, path, data, method='get', auth=True):
        encoded_data = urllib.parse.urlencode(data)

        if method == 'get':
            request_data = None
            request_url = '%s%s?%s' % (self.url, self._format_path(path), encoded_data)
        elif method == 'post':
            request_data = encoded_data.encode(DEFAULT_ENCODING)
            request_url = '%s%s' % (self.url, self._format_path(path))
        r = urllib.request.Request(request_url, data=request_data)
        if auth:
            r.add_header('Authorization', 'Bearer %s' % self.sessionkey)

        while True:
            try:
                f = urllib.request.urlopen(r)
                cont = f.read()
                f.close()
                break
            except KeyboardInterrupt:
                raise
            except urllib.error.URLError:
                raise
            except:
                print('Unexpected error:', sys.exc_info()[0])
                print('Will try again in %.2f seconds' % DEFAULT_RETRY_DELAY)
                time.sleep(DEFAULT_RETRY_DELAY)

        result_object = json.loads(cont.decode(DEFAULT_ENCODING))

        if result_object['_result']['status'] != 'ok':
            raise EliceResponseError(result_object)

        return json.loads(cont.decode(DEFAULT_ENCODING))

    def get(self, path, data, auth=True):
        return self.request(path, data, method='get', auth=auth)

    def post(self, path, data, auth=True):
        return self.request(path, data, method='post', auth=auth)

    def get_iter(self, path, data, extract_list, auth=True, offset=0, count=DEFAULT_COUNT):
        current_offset = offset
        while True:
            request_data = copy.copy(data)
            request_data['offset'] = current_offset
            request_data['count'] = count
            result = self.get(path, request_data, auth=auth)
            try:
                current_list = extract_list(result)
            except:
                ValueError('Failed to extract a list with given extract_list '
                    + ('from a result object fetched from the server: %s'
                    % json.dumps(result)))
                raise
            for item in current_list:
                yield item
            if len(current_list) < count:
                break
            current_offset += count

    def login(self, email, password, org=DEFAULT_ORGANIZATION_NAME):
        try:
            org_result = self.get('/common/organization/get/', {'organization_name_short': org}, auth=False)
        except EliceResponseError as error:
            if error.code == 'organization_not_exist':
                raise ValueError('Given organization name is not found on the server.')
            else:
                raise
        self.organization = org_result['organization']

        result = self.post('/auth/login/', {
            'organization_id': self.organization['id'],
            'email': email,
            'password': password
        }, auth=False)
        if 'sessionkey' in result:
            self.sessionkey = result['sessionkey']
        else:
            raise ValueError('Failed to login with given email and password.')

    def set_sessionkey(self, sessionkey):
        self.sessionkey = sessionkey
