# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from question_app.question_commands import ListQuestionCommand, SaveQuestionCommand, UpdateQuestionCommand, QuestionForm,\
    GetQuestionCommand, DeleteQuestionCommand


def save_question_cmd(**question_properties):
    """
    Command to save Question entity
    :param question_properties: a dict of properties to save on model
    :return: a Command that save Question, validating and localizing properties received as strings
    """
    return SaveQuestionCommand(**question_properties)


def update_question_cmd(question_id, **question_properties):
    """
    Command to update Question entity with id equals 'question_id'
    :param question_properties: a dict of properties to update model
    :return: a Command that update Question, validating and localizing properties received as strings
    """
    return UpdateQuestionCommand(question_id, **question_properties)


def list_questions_cmd():
    """
    Command to list Question entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListQuestionCommand()


def question_form(**kwargs):
    """
    Function to get Question's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return QuestionForm(**kwargs)


def get_question_cmd(question_id):
    """
    Find question by her id
    :param question_id: the question id
    :return: Command
    """
    return GetQuestionCommand(question_id)



def delete_question_cmd(question_id):
    """
    Construct a command to delete a Question
    :param question_id: question's id
    :return: Command
    """
    return DeleteQuestionCommand(question_id)

