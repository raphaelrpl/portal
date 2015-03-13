# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from question_app.question_model import Question



class QuestionSaveForm(ModelForm):
    """
    Form used to save and update Question
    """
    _model_class = Question
    _include = [Question.name, Question.user]


class QuestionForm(ModelForm):
    """
    Form used to expose Question's properties for list or json
    """
    _model_class = Question


class GetQuestionCommand(NodeSearch):
    _model_class = Question


class DeleteQuestionCommand(DeleteNode):
    _model_class = Question


class SaveQuestionCommand(SaveCommand):
    _model_form_class = QuestionSaveForm


class UpdateQuestionCommand(UpdateNode):
    _model_form_class = QuestionSaveForm


class ListQuestionCommand(ModelSearchCommand):
    def __init__(self):
        super(ListQuestionCommand, self).__init__(Question.query_by_creation())

