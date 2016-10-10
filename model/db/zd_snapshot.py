#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

from peewee import DateTimeField
from peewee import CharField
from peewee import TextField
from peewee import IntegerField
from peewee import SQL

from model.db.base import ZKDASH_DB, EnumField


class ZdSnapshot(ZKDASH_DB.Model):

    """ZdSnapshot Model
    """

    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    cluster_name = CharField(max_length=64, null=True)
    path = CharField(max_length=512, null=True)
    data = TextField(null=True)
    create_time = DateTimeField(null=True)
    commit = CharField(max_length=64, null=True)
    #operate_type = CharField(max_length=16, null=True)
    status = EnumField(enum_value="'0', '1'", constraints=[SQL("DEFAULT '0'")])
    deleted = EnumField(enum_value="'0', '1'", constraints=[SQL("DEFAULT '0'")])

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_snapshot"
