
python-elice
============

This simple client library is designed to support Elice API,
which allows developers to access all information available on its server.

You can browse available API endpoints at [API test panel](https://api-v4.elice.io/test/).

## How to use

### Elice

Elice class stores your session and allows you to access API endpoints with few methods.

* *`Elice(url=PRODUCTION_ELICE_API_URL)`*

    This creates an object from `Elice` class.
    Optional parameter `url` can be given when you want to communicate your own `elice-api` compatible server.

    **Example**

    ```
    from pyelice import Elice

    elice = Elice('http://johndoe.elicer.io:6663/')
    ```

* *`login(email, password)`*

    This logs in to Elice with given `email` and `password` as parameters.
    The session key will be retrieved and stored in the object.

    This raises `ValueError` when failed to log in with given parameters.

    **Example**

    ```
    elice.login('john_doe@elicer.io', 'naivepassword')
    ```

* *`set_sessionkey(sessionkey)`*

    This directly sets the session key for Elice.

    **Example**

    ```
    elice.set_sessionkey('wjeoiji2o3iwguhdujsnjvcoihwfe')
    ```

* *`get(path, data, auth=True)`*

    This performs a `GET` request to the given `path` with given parameters as `data`.
    Authentication token will be included in request's header when `auth` is true.

    **Example**

    ```
    result = self.get('/common/course/get/', {'course_id': 1})
    course = result['course']
    user_course_role = result['user_course_role']
    ```

* *`post(path, data, auth=True)`*

    This performs a `POST` request to the given `path` with given parameters as `data`.
    Authentication token will be included in request's header when `auth` is true.

    **Example**

    ```
    result = self.get('/common/board/article/edit/', {
        'board_id': 1,
        'title': 'Test article',
        'content': 'Hello world!\nThis is a test article',
        'is_secret': False
    })
    assert(result['_result']['status'] == 'ok')
    ```

* *`get_iter(path, data, extract_list, auth=True, offset=0, count=DEFAULT_COUNT)`*

    This returns a generator function that performs consecutive `GET` requests to the given `path`
    that accepts `count` and `offset` as parameters for paging.
    Given `extract_list` should be a function that takes a result object directly received from the server
    and returns a list of items that are expected. This method will yield an item at a time.

    When `offset` is given, this will start from the offset of given value. When `count` is given, this will request `count` items at a time.

    This raises `ValueError` when it has failed to extract a list from a result object received from the server.

    **Example**

    ```
    for user in elice.get_iter('/common/course/user/list/', { 'course_id': 1 }, lambda x: x['users']):
        print('%s %s' % (user['firstname'], user['lastname']))
    ```
