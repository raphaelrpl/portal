# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from notification_app.notification_model import Notification



class NotificationSaveForm(ModelForm):
    """
    Form used to save and update Notification
    """
    _model_class = Notification
    _include = [Notification.sender, Notification.user, Notification.message]


class NotificationForm(ModelForm):
    """
    Form used to expose Notification's properties for list or json
    """
    _model_class = Notification


class GetNotificationCommand(NodeSearch):
    _model_class = Notification


class DeleteNotificationCommand(DeleteNode):
    _model_class = Notification


class SaveNotificationCommand(SaveCommand):
    _model_form_class = NotificationSaveForm


class UpdateNotificationCommand(UpdateNode):
    _model_form_class = NotificationSaveForm


class ListNotificationCommand(ModelSearchCommand):
    def __init__(self):
        super(ListNotificationCommand, self).__init__(Notification.query_by_creation())

