#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

from peewee import DateTimeField
from peewee import CharField
from peewee import IntegerField
from peewee import SQL

from model.db.base import ZKDASH_DB, EnumField


class ZdFeedback(ZKDASH_DB.Model):

    """ZdFeedback Model
    """

    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    cluster = CharField(max_length=128, null=True)
    hostname = CharField(max_length=32, null=True)
    ip = CharField(max_length=32, null=True)
    path = CharField(max_length=512, null=True)
    value = CharField(max_length=128, null=True)
    update_time = DateTimeField(null=True)
    execute_status = EnumField(enum_value="'0', '1', '2'", constraints=[SQL("DEFAULT '0'")])
    deleted = EnumField(enum_value="'0', '1'", constraints=[SQL("DEFAULT '0'")])

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_feedback"
