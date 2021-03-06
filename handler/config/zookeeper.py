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
from lib.excel import ExcelWorkBook
from model.db.zd_zookeeper import ZdZookeeper
from model.db.zd_service import ZdService
from service import zookeeper as ZookeeperService
from conf import log


@route(r'/config/zookeeper/index', '查看')
class ZdZookeeperIndexHandler(CommonBaseHandler):

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
        clauses = self.parse_query(ZdZookeeper)
        order = getattr(ZdZookeeper, self.order_field)
        records = ZdZookeeper.select().order_by(
            getattr(order, self.order_direction)()
        ).where(reduce(operator.and_, clauses))
        self.render('config/zookeeper/index.html',
                    action='/config/zookeeper/index',
                    total=records.count(),
                    current_page=self.current_page,
                    page_size=self.page_size,
                    records=records.paginate(self.current_page, self.page_size))


@route(r'/config/zookeeper/show', '状态查看')
class ZdZookeeperViewHandler(CommonBaseHandler):

    '''index, 查看
    '''
    @authenticated
    def response(self):
        '''index
        '''
        zk_clusters = ZdZookeeper.select().where(
            ZdZookeeper.deleted == "0")
        self.render('config/zookeeper/stat.html',
                    zk_clusters=zk_clusters)


@route(r'/config/zookeeper/stat')
class ZdZookeeperStatHandler(CommonBaseHandler):

    """stat
    """
    args_list = [
        ArgsMap('host', required=True)
    ]

    @authenticated
    def response(self):
        """stat
        """
        cluster_info = ZookeeperService.get_stat(self.host)
        self.render('config/zookeeper/statdetail.html',
                    cluster_info=cluster_info)


@route(r'/config/zookeeper/search')
class ZdZookeeperSearchHandler(CommonBaseHandler):

    '''search,搜索
    '''
    args_list = [
        ArgsMap('pageSize', 'page_size', default=30),
        ArgsMap('pageCurrent', 'current_page', default=1),
        ArgsMap('orderDirection', 'order_direction', default="asc"),
        ArgsMap('orderField', 'order_field', default="id"),
    ]

    @authenticated
    def response(self):
        '''search
        '''
        clauses = self.parse_query(ZdZookeeper)
        order = getattr(ZdZookeeper, self.order_field)
        records = ZdZookeeper.select().order_by(
            getattr(order, self.order_direction)()
        ).where(reduce(operator.and_, clauses))
        self.render('config/zookeeper/datagrid.html',
                    total=records.count(),
                    current_page=self.current_page,
                    page_size=self.page_size,
                    records=records.paginate(self.current_page, self.page_size))


@route(r'/config/zookeeper/save')
class ZdZookeeperSaveHandler(CommonBaseHandler):
    """save
    """
    args_list = [
        ArgsMap('id', default=''),
        ArgsMap('cluster_name', default=''),
        ArgsMap('hosts', default=''),
        ArgsMap('business', default=''),
    ]

    @authenticated
    def response(self):
        '''add
        '''
        if self.id:
            # 修改记录
            tb_inst = ZdZookeeper.one(id=self.id)
        else:
            # 新增记录
            zookeeper = ZdZookeeper.one(cluster_name=self.cluster_name, deleted='0')
            # 检验集群名称是否重复
            if zookeeper:
                return self.ajax_popup(code=300, msg="zookeeper集群名称重复！")
            else:
                tb_inst = ZdZookeeper()
        if self.id:
            tb_inst.id = self.id
        if self.cluster_name:
            tb_inst.cluster_name = self.cluster_name
        if self.hosts:
            tb_inst.hosts = self.hosts
        if self.business:
            tb_inst.business = self.business
        tb_inst.save()
        return self.ajax_ok(forward="/config/zookeeper/index")


@route(r'/config/zookeeper/add', '新增')
class ZdZookeeperAddHandler(CommonBaseHandler):

    '''add, 新增
    '''

    @authenticated
    def response(self):
        '''add
        '''
        return self.render('config/zookeeper/add.html',
                           action='config/zookeeper/save')


@route(r'/config/zookeeper/edit', '修改')
class ZdZookeeperEditHandler(CommonBaseHandler):

    """edit, 修改
    """
    args_list = [
        ArgsMap('info_ids', default=''),
    ]

    def response(self):
        '''edit
        '''
        if self.info_ids:
            id_li = self.info_ids.split(',')
            if len(id_li) != 1:
                return self.ajax_popup(close_current=False, code=300, msg="请选择单条记录进行修改")
            record = ZdZookeeper.one(id=id_li[0])
            return self.render('config/zookeeper/edit.html',
                               action='/config/zookeeper/save',
                               record=record)
        else:
            return self.ajax_popup(close_current=False, code=300, msg="请选择某条记录进行修改")

@route(r'/config/zookeeper/query_services', '查询集群下面该用户有权限的所有子系统')
class ZdZookeeperQueryServicesHandler(CommonBaseHandler):

    """query_services, 查询集群下该用户有权限的所有子系统 
    """
    args_list = [
        ArgsMap('cluster', default=''),
    ]

    def response(self):
        zookeeper = ZdZookeeper.one(cluster_name=self.cluster, deleted='0')
        #self.set_header('Content-Type', 'application/json; charset=UTF-8')
        #self.write(json.dumps({'message': 'ok'}))
        #self.finish()
        if zookeeper is not None:
            services = ZdService.select().where((ZdService.zookeeper == zookeeper.id) & (ZdService.deleted == '0'))
            if services.count() >= 1:
                json_data = '{"service_names":['
                for service in services:
                    json_data += '"'
                    json_data += service.service_name
                    json_data += '",'
                json_data = json_data[0:len(json_data)-1]
                json_data += "]}"
                return json_data
	    else:
		json_data = ''
                self.finish()
	else:
            self.finish()
            #self.set_header('Content-Type', 'application/json; charset=UTF-8')
            #self.write(json.dumps(json_data))
            #self.finish()
        #'''edit
        #'''
        #if self.info_ids:
        #    id_li = self.info_ids.split(',')
        #    if len(id_li) != 1:
        #        return self.ajax_popup(close_current=False, code=300, msg="请选择单条记录进行修改")
        #    record = ZdZookeeper.one(id=id_li[0])
        #    return self.render('config/zookeeper/edit.html',
        #                       action='/config/zookeeper/save',
        #                       record=record)
        #else:
        #    return self.ajax_popup(close_current=False, code=300, msg="请选择某条记录进行修改")


#@route(r'/config/zookeeper/delete', '删除')
#class ZdZookeeperDeleteHandler(CommonBaseHandler):
#
#    """delete, 删除
#    """
#    args_list = [
#        ArgsMap('info_ids', default=''),
#    ]
#
#    def response(self):
#        '''delete
#        '''
#        if not self.info_ids:
#            return self.ajax_popup(close_current=False, code=300, msg="请选择某条记录进行删除")
#
#        id_list = self.info_ids.split(',')
#        try:
#            del_query = ZdZookeeper.delete().where(ZdZookeeper.id << id_list)
#            del_query.execute()
#        except OperationalError as exc:
#            log.error("error occurred while delete zookeepers, ids: %s\n%s", id_list, str(exc))
#            return self.ajax_popup(close_current=False, code=300, msg="删除失败！")
#        return self.ajax_ok(close_current=False)

@route(r'/config/zookeeper/delete', '删除')
class ZdZookeeperDeleteHandler(CommonBaseHandler):

    """delete, 删除
    """
    args_list = [
        ArgsMap('info_ids', default=''),
    ]

    def response(self):
        '''delete
        '''
        if not self.info_ids:
            return self.ajax_popup(close_current=False, code=300, msg="请选择某条记录进行删除")

        id_list = self.info_ids.split(',')
        for zookeeper_id in id_list:
            zookeeper = ZdZookeeper.one(id=zookeeper_id)
            zookeeper.deleted = '1'
            zookeeper.save()
            services = ZdService.select().where(ZdService.zookeeper == zookeeper.id and ZdService.deleted == '0')
            for service in services:
                service.deleted = '1'
                service.save()
        return self.ajax_ok(close_current=False)


@route(r'/config/zookeeper/export', '导出')
class ZdZookeeperExportHandler(CommonBaseHandler):

    """export,导出数据到excel
    """
    args_list = [
        ArgsMap('info_ids', default=''),
    ]

    def response(self):
        '''导出选中数据到excel中
        '''
        id_li = self.info_ids.split(',')
        sheet_text = ZdZookeeper.select().where(ZdZookeeper.id << id_li)
        sheet_title = [
            {'name': '集群名称'},
            {'name': '集群配置'},
            {'name': '集群业务'},
        ]
        bind_attr = (
            'cluster_name',
            'hosts',
            'business',
        )
        ewb = ExcelWorkBook()
        sheet_name = ZdZookeeper._meta.db_table
        ewb.add_sheet(sheet_name)
        ewb.add_title(sheet_name, sheet_title)
        ewb.add_text(sheet_name, sheet_text, bind=bind_attr)
        filename = '{}.xls'.format(sheet_name)
        filename = urllib.urlencode({'filename': filename})
        self.set_header('Content-Disposition', 'attachment;{}'.format(filename))
        self.finish(ewb.get_stream())
