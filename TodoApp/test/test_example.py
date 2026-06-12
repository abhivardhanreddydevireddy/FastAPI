import pytest
from fastapi.openapi.utils import validation_error_definition


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 2

def test_is_instance():
    assert isinstance( 'this is a string', str)
    assert not isinstance('10', int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello'=='world') is False

def test_type():
    assert type("hello" is str)
    assert type('world' is not int)

def test_grater_and_less_than():
    assert True == True

    assert 3 < 7

def test_list():
    num_list = [1,2,3]
    any_list = [False,False]
    assert 1 in num_list
    assert 5  not in num_list
    assert any_list == [False,False]


   
class Student():
    def __init__(self,first_name:str,last_name:str,major:str,years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years



@pytest.fixture
def default_employee():
    return Student('john','doe','cse',3)
def test_person_initialization(default_employee):
    p = Student('jhon','deo','cse',3)
    assert p.first_name == 'jhon' ,'First name should be jhon'
    assert p.last_name == 'deo' ,'last name should be deo'
    assert p.major == 'cse'

