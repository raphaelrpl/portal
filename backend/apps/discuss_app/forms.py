# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaeforms.ndb.form import ModelForm
from gaeforms.base import StringField
from gaepermission.model import MainUser


class UserForm(ModelForm):
    _model_class = MainUser
    confirm = StringField(required=True)

    def validate_password(self):
        if self._fields['confirm'] != self._fields['password']:
            return False
        return True

    def validate(self):
        errors = super(UserForm, self).validate()
        if self._fields['confirm'] != self._fields['password']:
            errors['confirm'] = "Password does not match"
        return errors
