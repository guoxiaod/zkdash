#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

from peewee import CharField
from peewee import IntegerField
from peewee import SQL

from model.db.base import ZKDASH_DB, EnumField


class ZdUser(ZKDASH_DB.Model):

    """ZdZnode Model
    """

    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    username = CharField(max_length=64, null=True)
    password = CharField(max_length=64, null=True)
    deleted = EnumField(enum_value="'0', '1'", constraints=[SQL("DEFAULT '0'")])

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_user"
