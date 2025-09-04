import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    
def test_create_choice_with_empty_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*300, False)
        
def test_remove_choice():
    question = Question(title='q1')
    choice = question.add_choice('a', False)
    
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.remove_choice(999)
    with pytest.raises(Exception):
        question.remove_choice('invalid_id')
    
def test_remove_choice_with_no_choices():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.remove_choice(1)

def test_set_correct_choice():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    assert choice1.is_correct == False
    assert choice2.is_correct == True

    question.set_correct_choices([choice1.id])
    assert choice1.is_correct == True
    assert choice2.is_correct == True

def test_generate_choice_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    
    assert choice1.id == 1
    assert choice2.id == 2
    
def test_find_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('a', False)
    
    found_choice = question._find_choice_by_id(choice.id)
    assert found_choice == choice
    
def test_valid_choice_id():
    question = Question(title='q1')
    choice = question.add_choice('a', False)

    with pytest.raises(Exception):
        question._check_valid_choice_id(999)
    with pytest.raises(Exception):
        question._check_valid_choice_id('invalid_id')

def test_find_correct_choice_ids():
    question = Question(title='q1')
    question.add_choice('a', True)
    question.add_choice('b', False)
    
    correct_ids = question._find_correct_choice_ids()
    assert correct_ids == [1]

def test_list_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    
    choices = question._list_choice_ids()
    assert len(choices) == 2
    assert question._find_choice_by_id(choices[0]).text == 'a'
    assert question._find_choice_by_id(choices[1]).text == 'b'
