# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaeforms.ndb.form import ModelForm
from gaepermission.model import MainUser


class MainUserForm(ModelForm):
    _model_class = MainUser