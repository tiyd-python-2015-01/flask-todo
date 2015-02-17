import pytest
import to_do


def test_create_db():
    to_do.init_db()
    if '/tmp/to_do.db':
        assert True

def test_add_task():
    task = 'take dog out'
    to_do.add_task(task)
    assert task in '/tmp/to_do.db'

def test_get_tasks():
    to_do.add_task('take dog out')
    assert to_do.get_tasks()[1] == 'take dog out'

def test_delete_task():
    to_do.add_task('take dog out')
    to_do.delete_task(get_tasks()[0])
    assert to_do.get_tasks == False
