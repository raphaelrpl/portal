# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from comment_app.comment_commands import ListCommentCommand, SaveCommentCommand, UpdateCommentCommand, CommentForm,\
    GetCommentCommand, DeleteCommentCommand


def save_comment_cmd(**comment_properties):
    """
    Command to save Comment entity
    :param comment_properties: a dict of properties to save on model
    :return: a Command that save Comment, validating and localizing properties received as strings
    """
    return SaveCommentCommand(**comment_properties)


def update_comment_cmd(comment_id, **comment_properties):
    """
    Command to update Comment entity with id equals 'comment_id'
    :param comment_properties: a dict of properties to update model
    :return: a Command that update Comment, validating and localizing properties received as strings
    """
    return UpdateCommentCommand(comment_id, **comment_properties)


def list_comments_cmd():
    """
    Command to list Comment entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListCommentCommand()


def comment_form(**kwargs):
    """
    Function to get Comment's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return CommentForm(**kwargs)


def get_comment_cmd(comment_id):
    """
    Find comment by her id
    :param comment_id: the comment id
    :return: Command
    """
    return GetCommentCommand(comment_id)



def delete_comment_cmd(comment_id):
    """
    Construct a command to delete a Comment
    :param comment_id: comment's id
    :return: Command
    """
    return DeleteCommentCommand(comment_id)

