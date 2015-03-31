# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from permission_app.permission_commands import MainUserForm


def main_user_form(**kwargs):
    """
    Function to get Comment's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return MainUserForm(**kwargs)