# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from badge_app.badge_commands import ListBadgeCommand, SaveBadgeCommand, UpdateBadgeCommand, BadgeForm,\
    GetBadgeCommand, DeleteBadgeCommand


def save_badge_cmd(**badge_properties):
    """
    Command to save Badge entity
    :param badge_properties: a dict of properties to save on model
    :return: a Command that save Badge, validating and localizing properties received as strings
    """
    return SaveBadgeCommand(**badge_properties)


def update_badge_cmd(badge_id, **badge_properties):
    """
    Command to update Badge entity with id equals 'badge_id'
    :param badge_properties: a dict of properties to update model
    :return: a Command that update Badge, validating and localizing properties received as strings
    """
    return UpdateBadgeCommand(badge_id, **badge_properties)


def list_badges_cmd():
    """
    Command to list Badge entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListBadgeCommand()


def badge_form(**kwargs):
    """
    Function to get Badge's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return BadgeForm(**kwargs)


def get_badge_cmd(badge_id):
    """
    Find badge by her id
    :param badge_id: the badge id
    :return: Command
    """
    return GetBadgeCommand(badge_id)



def delete_badge_cmd(badge_id):
    """
    Construct a command to delete a Badge
    :param badge_id: badge's id
    :return: Command
    """
    return DeleteBadgeCommand(badge_id)

