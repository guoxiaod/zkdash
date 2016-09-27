#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: feedback.py
创 建 者: zhuangshixiong
创建日期: 2015-06-24
"""
from datetime import datetime

from handler.bases import ApiBaseHandler
from handler.bases import ArgsMap
from lib import route
from model.db.zd_qconf_feedback import ZdQconfFeedback
import json


@route(r'/api/v1/feedback')
class ZdQconfFeedbackSaveHandler(ApiBaseHandler):
    """save
    """
    args_list = [
        ArgsMap('id', default=''),
        ArgsMap('cluster', default=''),
        ArgsMap('hostname', default=''),
        ArgsMap('ip', default=''),
        #ArgsMap('path', default=''),
        #ArgsMap('value', default=''),
        #ArgsMap('update_time', default=''),
        #ArgsMap('deleted', default=''),
        ArgsMap('time', default=''),
        ArgsMap('values', default=''),
    ]

    def response(self):
        '''add
        '''
	path2values = json.loads(self.values)
	for path, value in path2values.items():
            feedback = ZdQconfFeedback.one(cluster=self.cluster, ip=self.ip, path=path)
            if feedback is None:
                # create new feedback record
                feedback = ZdQconfFeedback()
            # 填充字段
            if self.cluster:
                feedback.cluster = self.cluster
            if self.hostname:
                feedback.hostname = self.hostname
            if self.ip:
                feedback.ip = self.ip
            if path:
                feedback.path = path
            if self.time:
                # convert unix timestamp to datetime
                update_time = datetime.fromtimestamp(
                    int(self.time)).strftime('%Y-%m-%d %H:%M:%S')
                feedback.update_time = update_time
            if value:
                feedback.value = value
            feedback.save()
        # qconf protocol, return '0' means ok
        self.finish('0')
