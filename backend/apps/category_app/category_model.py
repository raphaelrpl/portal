# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from unidecode import unidecode
import re


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return unicode(delim.join(result))


class Category(Node):
    name = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True)

    @classmethod
    def is_available_slug(cls, slug):
        return Category.query(Category.slug == slug).count()

    def _pre_put_hook(self):
        self.slug = slugify(unicode(self.name))
        if self.is_available_slug(self.slug) != 0:
            self.slug = None
        super(Category, self)._pre_put_hook()