#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import urllib
import operator
import json
from tornado.web import authenticated
import tornado.escape
from peewee import OperationalError

from handler.bases import CommonBaseHandler
from handler.bases import ArgsMap
from lib import route
from lib.utils.hashutil import HashUtil
from lib.excel import ExcelWorkBook
from model.db.zd_zookeeper import ZdZookeeper
from model.db.zd_user import ZdUser
from model.db.zd_service import ZdService
from service import zookeeper as ZookeeperService
from conf import log

@route(r'/config/user/index', '查看')
class ZdUserIndexHandler(CommonBaseHandler):

    '''index, 查看
    '''
    args_list = [
        ArgsMap('pageSize', 'page_size', default=30),
        ArgsMap('pageCurrent', 'current_page', default=1),
        ArgsMap('orderDirection', 'order_direction', default="asc"),
        ArgsMap('orderField', 'order_field', default="id"),
    ]

    @authenticated
    def response(self):
        '''index
        '''
        clauses = self.parse_query(ZdUser)
        order = getattr(ZdUser, self.order_field)
        records = ZdUser.select().order_by(
            getattr(order, self.order_direction)()
        ).where(reduce(operator.and_, clauses))
        self.render('config/user/index.html',
                    action='/config/user/index',
                    total=records.count(),
                    current_page=self.current_page,
                    page_size=self.page_size,
                    records=records.paginate(self.current_page, self.page_size))

@route(r'/config/user/search', '查看')
class ZdUserSearchHandler(CommonBaseHandler):

    '''search, 查看
    '''
    args_list = [
        ArgsMap('pageSize', 'page_size', default=30),
        ArgsMap('pageCurrent', 'current_page', default=1),
        ArgsMap('orderDirection', 'order_direction', default="asc"),
        ArgsMap('orderField', 'order_field', default="id"),
        ArgsMap('username', default=''),
    ]

    @authenticated
    def response(self):
        '''index
        '''
        clauses = self.parse_query(ZdUser)
        order = getattr(ZdUser, self.order_field)
        records = ZdUser.select().where((ZdUser.username==self.username) & (ZdUser.deleted=='0'))
        #records = ZdUser.select().order_by(
        #    getattr(order, self.order_direction)()
        #).where(reduce(operator.and_, clauses))
        self.render('config/user/datagrid.html',
                    total=records.count(),
                    current_page=self.current_page,
                    page_size=self.page_size,
                    records=records.paginate(self.current_page, self.page_size))

@route(r'/config/user/add', '新增')
class ZdUserAddHandler(CommonBaseHandler):

    '''add, 新增
    '''

    @authenticated
    def response(self):
        '''add
        '''
        result = dict()
        zookeepers = ZdZookeeper.select().where(ZdZookeeper.deleted == '0')
        for zookeeper in zookeepers:
            services = ZdService.select().where((ZdService.zookeeper == zookeeper.id) & (ZdService.deleted == '0'))
            result[zookeeper] = services
        return self.render('config/user/add.html',
                           action='config/user/save',
                           result=result)

@route(r'/config/user/edit', '修改')
class ZdUserEditHandler(CommonBaseHandler):

    '''edit, 修改
    '''
    args_list = [
        ArgsMap('info_ids', default=''),
    ]

    @authenticated
    def response(self):
        '''edit
        '''
        if self.info_ids:
            id_li = self.info_ids.split(',')
            if len(id_li) != 1:
                return self.ajax_popup(close_current=False, code=300, msg="请选择单条记录进行修改")
            else:
                user = ZdUser.one(id=id_li[0], deleted='0')
                result = dict()
                zookeepers = ZdZookeeper.select().where(ZdZookeeper.deleted == '0')
                for zookeeper in zookeepers:
                    services = ZdService.select().where((ZdService.zookeeper == zookeeper.id) & (ZdService.deleted == '0'))
                    result[zookeeper] = services
                return self.render('config/user/edit.html',
                                   action='config/user/save',
                                   user=user,
                                   result=result)
        else:
            return self.ajax_popup(close_current=False, code=300, msg="请选择某条记录进行修改")

@route(r'/config/user/save', '新增')
class ZdUserSaveHandler(CommonBaseHandler):

    '''add, 新增
    '''
    args_list = [
        ArgsMap('id', default=''),
        ArgsMap('username', default=''),
        ArgsMap('password', default=''),
    ]

    @authenticated
    def response(self):
        '''save
        '''
        if self.id:
            user = ZdUser.one(id=self.id, deleted='0')
        else:
            user = ZdUser.one(username=self.username, deleted='0')
            if user:
                return self.ajax_popup(code=300, msg="用户名重复！")
            else:
                user = ZdUser()

        if self.id:
            user.id = self.id
        if self.username:
            user.username = self.username
        if self.password:
            user.password = HashUtil().sha1(self.password)

        service_ids = self.get_arguments("service_id")
        permission = ''
        for service_id in service_ids:
            permission = permission + service_id + ':'
        user.permission= permission

        user.save()
        return self.ajax_ok(forward="/config/user/index")

@route(r'/config/user/delete', '删除')
class ZdUserDeleteHandler(CommonBaseHandler):

    '''delete, 删除
    '''
    args_list = [
        ArgsMap('info_ids', default=''),
    ]

    @authenticated
    def response(self):
        '''delete
        '''
        if self.info_ids:
            id_li = self.info_ids.split(',')
            if len(id_li) != 1:
                return self.ajax_popup(close_current=False, code=300, msg="请选择单条记录进行修改")
            else:
                user = ZdUser.one(id=id_li[0], deleted='0')
                user.deleted = '1'
                user.save()
                return self.ajax_ok(forward="config/user/index")
        else:
            return self.ajax_popup(close_current=False, code=300, msg="请选择某条记录进行修改")
