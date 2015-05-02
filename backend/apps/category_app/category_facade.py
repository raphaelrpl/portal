# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from category_app.category_commands import ListCategoryCommand, SaveCategoryCommand, UpdateCategoryCommand, CategoryForm,\
    GetCategoryCommand, DeleteCategoryCommand


def save_category_cmd(**category_properties):
    """
    Command to save Category entity
    :param category_properties: a dict of properties to save on model
    :return: a Command that save Category, validating and localizing properties received as strings
    """
    return SaveCategoryCommand(**category_properties)


def update_category_cmd(category_id, **category_properties):
    """
    Command to update Category entity with id equals 'category_id'
    :param category_properties: a dict of properties to update model
    :return: a Command that update Category, validating and localizing properties received as strings
    """
    return UpdateCategoryCommand(category_id, **category_properties)


def list_categorys_cmd():
    """
    Command to list Category entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListCategoryCommand()


def category_form(**kwargs):
    """
    Function to get Category's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return CategoryForm(**kwargs)


def get_category_cmd(category_id):
    """
    Find category by her id
    :param category_id: the category id
    :return: Command
    """
    return GetCategoryCommand(category_id)



def delete_category_cmd(category_id):
    """
    Construct a command to delete a Category
    :param category_id: category's id
    :return: Command
    """
    return DeleteCategoryCommand(category_id)

