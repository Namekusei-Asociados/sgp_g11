# we define a fixture function below and it will be "used" by
# referencing its name from tests

import pytest


@pytest.fixture(scope="class")
def db_class(request):
    class DummyDB:
        pass

    # set a class attribute on the invoking test context
    request.cls.db = DummyDB()
