# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from notification_app.notification_commands import ListNotificationCommand, SaveNotificationCommand, UpdateNotificationCommand, NotificationForm,\
    GetNotificationCommand, DeleteNotificationCommand


def save_notification_cmd(**notification_properties):
    """
    Command to save Notification entity
    :param notification_properties: a dict of properties to save on model
    :return: a Command that save Notification, validating and localizing properties received as strings
    """
    return SaveNotificationCommand(**notification_properties)


def update_notification_cmd(notification_id, **notification_properties):
    """
    Command to update Notification entity with id equals 'notification_id'
    :param notification_properties: a dict of properties to update model
    :return: a Command that update Notification, validating and localizing properties received as strings
    """
    return UpdateNotificationCommand(notification_id, **notification_properties)


def list_notifications_cmd():
    """
    Command to list Notification entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListNotificationCommand()


def notification_form(**kwargs):
    """
    Function to get Notification's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return NotificationForm(**kwargs)


def get_notification_cmd(notification_id):
    """
    Find notification by her id
    :param notification_id: the notification id
    :return: Command
    """
    return GetNotificationCommand(notification_id)



def delete_notification_cmd(notification_id):
    """
    Construct a command to delete a Notification
    :param notification_id: notification's id
    :return: Command
    """
    return DeleteNotificationCommand(notification_id)

