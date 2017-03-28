
python-elice
============

This simple client library is designed to support Elice API,
which allows developers to access all information available on its server.

You can browse available API endpoints at [API test panel](https://api-v4.elice.io/test/).

## How to use

### Install

Before installing the library, please make sure to register your SSH key on this Gitlab server.
Otherwise, you will not be allowed to install this project from this server.

Run:
```
$ pip install git+ssh://git@git.elicer.io:2201/elice/python-elice.git
```
to install `python-elice` on your local environment.

If you have already installed the older version and want to install the latest version, run:
```
$ pip install --upgrade git+ssh://git@git.elicer.io:2201/elice/python-elice.git
```

### Elice

`Elice` class stores your session and allows you to access API endpoints with few methods.

* *`Elice(url=PRODUCTION_ELICE_API_URL)`*

    This creates an object from `Elice` class.
    Optional parameter `url` can be given when you want to communicate your own `elice-api` compatible server.

    **Example**

    ```python
    from pyelice import Elice, EliceResponseError

    elice = Elice('http://johndoe.elicer.io:6663/')
    ```

* *`login(email, password, org='academy')`*

    This logs in to Elice's `organization` with given `email` and `password`.
    The session key will be retrieved and stored in the object.

    This raises `ValueError` when failed to log in with given parameters.

    **Example**

    ```python
    elice.login('john_doe@elicer.io', 'naivepassword', 'academy')
    ```

* *`set_sessionkey(sessionkey)`*

    This directly sets the session key for Elice.

    **Example**

    ```python
    elice.set_sessionkey('wjeoiji2o3iwguhdujsnjvcoihwfe')
    ```

* *`get(path, data, auth=True)`*

    This performs a `GET` request to the given `path` with given parameters as `data`.
    Authentication token will be included in request's header when `auth` is true.

    This raises `EliceResponseError` when the server returns an object with error information.

    **Example**

    ```python
    result = self.get('/common/course/get/', {'course_id': 1})
    course = result['course']
    user_course_role = result['user_course_role']
    ```

* *`post(path, data, auth=True)`*

    This performs a `POST` request to the given `path` with given parameters as `data`.
    Authentication token will be included in request's header when `auth` is true.

    This raises `EliceResponseError` when the server returns an object with error information.

    **Example**

    ```python
    try:
      result = self.get('/common/board/article/edit/', {
          'board_id': 1,
          'title': 'Test article',
          'content': 'Hello world!\nThis is a test article',
          'is_secret': False
      })
    except EliceResponseError:
      print('Failed to write an article.')
    ```

* *`get_iter(path, data, extract_list, auth=True, offset=0, count=DEFAULT_COUNT)`*

    This returns a generator function that performs consecutive `GET` requests to the given `path`
    that accepts `count` and `offset` as parameters for paging.
    Given `extract_list` should be a function that takes a result object directly received from the server
    and returns a list of items that are expected. This method will yield an item at a time.

    When `offset` is given, this will start from the offset of given value. When `count` is given, this will request `count` items at a time.

    This raises `ValueError` when it has failed to extract a list from a result object received from the server.

    **Example**

    ```python
    for user in elice.get_iter('/common/course/user/list/', { 'course_id': 1 }, lambda x: x['users']):
        print('%s %s' % (user['firstname'], user['lastname']))
    ```

### EliceResponseError

`EliceResponseError` class extends `Exception` and contains error object retrieved from the server.

* *`message`*

    Member variable `message` contains a fail message extracted from the object.

    **Example**

    ```python
    try:
      result = self.get('/common/course/get/', {'course_id': 1})
    except EliceResponseError as error:
      print(error.message)
      # invalid parameter exists
    ```

* *`code`*

    Member variable `code` contains a fail code extracted from the object.
    The value is `unknown` when unexpected object is retrieved.

    **Example**

    ```python
    try:
      result = self.get('/common/organization/get/', {'organization_name_short': 'blah'})
    except EliceResponseError as error:
      print(error.code)
      # organization_not_exist
    ```

* *`body`*

    Member variable `body` contains a full error object retrieved from the server.

    **Example**

    ```python
    try:
      result = self.get('/common/course/get/', {'course_id': 1})
    except EliceResponseError as error:
      print(error.body)
      # {
      #     "_result": {
      #         "reason": "param",
      #         "status": "fail"
      #     },
      #     "fail_detail": {
      #         "course_id": "does not exist"
      #     },
      #     "fail_message": "invalid parameter exists"
      # }
    ```
