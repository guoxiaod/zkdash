#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: service.py
创 建 者: baipeng
创建日期: 2016-09-12
"""
import os
import hashlib

import json
import operator
from tornado.web import authenticated
from kazoo.exceptions import NotEmptyError, BadArgumentsError

from handler.bases import CommonBaseHandler
from handler.bases import ArgsMap
from lib import route
from lib.utils import normalize_path
from model.db.zd_znode import ZdZnode
from model.db.zd_zookeeper import ZdZookeeper
from model.db.zd_service import ZdService
from model.db.zd_qconf_feedback import ZdQconfFeedback
from service import zookeeper as ZookeeperService
from service import znode as ZnodeService
from conf.settings import USE_QCONF


############################################################
# UI
############################################################

@route(r'/config/service/index', '查看')
class ZdServiceIndexHandler(CommonBaseHandler):

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
        # zookeeper clusters
        clusters = ZdZookeeper.select().where(ZdZookeeper.deleted == "0")
        if clusters.count() < 1:
            return self.ajax_popup(code=300, msg="请先到zookeeper管理菜单下设置集群信息！")
        clauses = self.parse_query(ZdService)
        order = getattr(ZdService, self.order_field)
        records = ZdService.select().order_by(
            getattr(order, self.order_direction)()
        ).where(reduce(operator.and_, clauses))
        self.render('config/service/index.html',
                    action='/config/service/index',
                    total=records.count(),
                    current_page=self.current_page,
                    page_size=self.page_size,
                    records=records.paginate(self.current_page, self.page_size))


@route(r'/config/service/add', '新增')
class ZdServiceAddHandler(CommonBaseHandler):

    '''add, 新增
    '''

    @authenticated
    def response(self):
        '''add
        '''
        return self.render('config/service/add.html',
                           action='config/service/save')

@route(r'/config/service/save')
class ZdServiceSaveHandler(CommonBaseHandler):
    """save
    """
    args_list = [
        ArgsMap('id', default=''),
        ArgsMap('cluster_name', default=''),
        ArgsMap('service_name', default=''),
    ]

    @authenticated
    def response(self):
        '''add
        '''
        if self.id:
            # 修改记录
            tb_inst = ZdService.one(id=self.id)
        else:
            zookeeper = ZdZookeeper.one(cluster_name=self.cluster_name, deleted='0')
            if zookeeper is None:
                return self.ajax_popup(code=300, msg="zookeeper名称错误！")
            else:
                # 新增记录
                service = ZdService.one(zookeeper_id=zookeeper.id, service_name=self.service_name, deleted='0')
                # 检验集群下是否已经有该服务
                if service:
                    return self.ajax_popup(code=300, msg="service名称重复！")
                else:
                    tb_inst = ZdService()
        if self.id:
            tb_inst.id = self.id
        if self.cluster_name:
            tb_inst.cluster_name = self.cluster_name
        if self.service_name:
            tb_inst.service_name = self.service_name
        tb_inst.save()
        return self.ajax_ok(forward="/config/service/index")
