# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from discuss_app.discuss_model import Discuss



class DiscussSaveForm(ModelForm):
    """
    Form used to save and update Discuss
    """
    _model_class = Discuss
    _include = [Discuss.content, 
                Discuss.title,
                Discuss.user]


class DiscussForm(ModelForm):
    """
    Form used to expose Discuss's properties for list or json
    """
    _model_class = Discuss


class GetDiscussCommand(NodeSearch):
    _model_class = Discuss


class DeleteDiscussCommand(DeleteNode):
    _model_class = Discuss


class SaveDiscussCommand(SaveCommand):
    _model_form_class = DiscussSaveForm


class UpdateDiscussCommand(UpdateNode):
    _model_form_class = DiscussSaveForm


class ListDiscussCommand(ModelSearchCommand):
    def __init__(self):
        super(ListDiscussCommand, self).__init__(Discuss.query_by_creation())

