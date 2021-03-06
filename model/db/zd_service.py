#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

from peewee import DateTimeField
from peewee import CharField
from peewee import TextField
from peewee import IntegerField
from peewee import ForeignKeyField
from peewee import SQL

from model.db.base import ZKDASH_DB, EnumField
from model.db.zd_zookeeper import ZdZookeeper

class ZdService(ZKDASH_DB.Model):

    """ZdService Model
    """

    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    service_name = CharField(max_length=64, null=True)
    #zookeeper_id = IntegerField()
    #related_name反向引用名称,可以用zookeeper.services访问关联的所有服务
    zookeeper = ForeignKeyField(ZdZookeeper, related_name='services')
    #path = CharField(max_length=512, null=True)
    #data = TextField(null=True)
    #create_time = DateTimeField(null=True)
    #commit = CharField(max_length=64, null=True)
    #status = EnumField(enum_value="'0', '1'", constraints=[SQL("DEFAULT '0'")])
    deleted = EnumField(enum_value="'0', '1'", constraints=[SQL("DEFAULT '0'")])

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_service"
