# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime


class FriendlyDatetime(object):
    messages = {"days": "Há %s dia", "hours": "Há %s hora", "mins": "Há %s minuto", "secs": "Há %s segundo"}

    def __init__(self, fmt=None):
        self.format = fmt

    def __call__(self, date):
        today = datetime.now()
        result = today - date
        if result.days > 0:
            return self.messages['days'] % result.days
        hours = result.seconds / 3600
        if hours > 0:
            return self.messages['hours'] % hours
        minutes = result.seconds / 60
        if hours > 0:
            return self.messages['mins'] % minutes
        return self.messages['secs'] % result.seconds