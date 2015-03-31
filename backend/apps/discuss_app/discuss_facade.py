# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from discuss_app.discuss_commands import ListDiscussCommand, SaveDiscussCommand, UpdateDiscussCommand, DiscussForm,\
    GetDiscussCommand, DeleteDiscussCommand


def save_discuss_cmd(**discuss_properties):
    """
    Command to save Discuss entity
    :param discuss_properties: a dict of properties to save on model
    :return: a Command that save Discuss, validating and localizing properties received as strings
    """
    return SaveDiscussCommand(**discuss_properties)


def update_discuss_cmd(discuss_id, **discuss_properties):
    """
    Command to update Discuss entity with id equals 'discuss_id'
    :param discuss_properties: a dict of properties to update model
    :return: a Command that update Discuss, validating and localizing properties received as strings
    """
    return UpdateDiscussCommand(discuss_id, **discuss_properties)


def list_discusss_cmd():
    """
    Command to list Discuss entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListDiscussCommand()


def discuss_form(**kwargs):
    """
    Function to get Discuss's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return DiscussForm(**kwargs)


def get_discuss_cmd(discuss_id):
    """
    Find discuss by her id
    :param discuss_id: the discuss id
    :return: Command
    """
    return GetDiscussCommand(discuss_id)



def delete_discuss_cmd(discuss_id):
    """
    Construct a command to delete a Discuss
    :param discuss_id: discuss's id
    :return: Command
    """
    return DeleteDiscussCommand(discuss_id)

