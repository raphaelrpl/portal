# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from badge_app.badge_model import Badge



class BadgeSaveForm(ModelForm):
    """
    Form used to save and update Badge
    """
    _model_class = Badge
    _include = [Badge.name]


class BadgeForm(ModelForm):
    """
    Form used to expose Badge's properties for list or json
    """
    _model_class = Badge


class GetBadgeCommand(NodeSearch):
    _model_class = Badge


class DeleteBadgeCommand(DeleteNode):
    _model_class = Badge


class SaveBadgeCommand(SaveCommand):
    _model_form_class = BadgeSaveForm


class UpdateBadgeCommand(UpdateNode):
    _model_form_class = BadgeSaveForm


class ListBadgeCommand(ModelSearchCommand):
    def __init__(self):
        super(ListBadgeCommand, self).__init__(Badge.query_by_creation())

