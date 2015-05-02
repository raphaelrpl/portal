# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from category_app.category_model import Category



class CategorySaveForm(ModelForm):
    """
    Form used to save and update Category
    """
    _model_class = Category
    _include = [Category.slug, 
                Category.name]


class CategoryForm(ModelForm):
    """
    Form used to expose Category's properties for list or json
    """
    _model_class = Category


class GetCategoryCommand(NodeSearch):
    _model_class = Category


class DeleteCategoryCommand(DeleteNode):
    _model_class = Category


class SaveCategoryCommand(SaveCommand):
    _model_form_class = CategorySaveForm


class UpdateCategoryCommand(UpdateNode):
    _model_form_class = CategorySaveForm


class ListCategoryCommand(ModelSearchCommand):
    def __init__(self):
        super(ListCategoryCommand, self).__init__(Category.query_by_creation())

