# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from comment_app.comment_model import Comment, ReplyComment


class ReplyCommentSaveForm(ModelForm):
    _model_class = ReplyComment
    _include = [ReplyComment.comment, ReplyComment.user, ReplyComment.content]


class ReplyCommentForm(ModelForm):
    _model_class = ReplyComment


class GetReplyCommentCommand(NodeSearch):
    _model_class = ReplyComment


class DeleteReplyCommentCommand(DeleteNode):
    _model_class = ReplyComment


class SaveReplyCommentCommand(SaveCommand):
    _model_form_class = ReplyCommentSaveForm


class UpdateReplyCommentCommand(UpdateNode):
    _model_form_class = ReplyCommentSaveForm


class ListReplyCommentCommand(ModelSearchCommand):
    def __init__(self):
        super(ListReplyCommentCommand, self).__init__(ReplyComment.query_by_creation())


# ################### COMMENT AREA ###################
class CommentSaveForm(ModelForm):
    _model_class = Comment
    _include = [Comment.content, Comment.user, Comment.post]


class CommentForm(ModelForm):
    """
    Form used to expose Comment's properties for list or json
    """
    _model_class = Comment


class GetCommentCommand(NodeSearch):
    _model_class = Comment


class DeleteCommentCommand(DeleteNode):
    _model_class = Comment


class SaveCommentCommand(SaveCommand):
    _model_form_class = CommentSaveForm


class UpdateCommentCommand(UpdateNode):
    _model_form_class = CommentSaveForm


class ListCommentCommand(ModelSearchCommand):
    def __init__(self):
        super(ListCommentCommand, self).__init__(Comment.query_by_creation())

