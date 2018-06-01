#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: index.py
创 建 者: zhuangshixiong
创建日期: 2015-10-09
"""
from handler.bases import CommonBaseHandler
from lib import route
from lib.utils.hashutil import HashUtil
from model.db.zd_user import ZdUser


@route(r'/')
class IndexHandler(CommonBaseHandler):

    '''配置管理系统页面入口
    '''

    #def response(self):
    #    return self.render('index.html')

    def response(self):
        if self.current_user :
            return self.render('index.html', current_user = self.current_user)

        return self.render('login.html', message = '')

@route(r'/logout', '退出登录')
class LogoutMainHandler(CommonBaseHandler):
    def response(self):
        try:
            self.set_cookie("user", '', expires = -1)
        except Exception:
            pass
        return self.render('login.html', message = '')

@route(r'/login', '登录验证')
class LoginMainHandler(CommonBaseHandler):

    '''首页
    '''

    def response(self):
        try:
            method = self.get_method()
            if method == 'GET' and self.current_user:
                return self.redirect('/')
            elif method == "POST":
                username = self.get_argument('username')
                password = self.get_argument('passwordhash')

                if username and password:
                    password = HashUtil().sha1(password)
                    records = ZdUser.select().where((ZdUser.username == username) & (ZdUser.password == password))

                    if records.count() > 0:
                        self.set_secure_cookie('user', username)
                        return self.render('index.html', current_user = username)
                raise ValueError(u'用户名或者密码错误')
        except Exception as error:
            return self.render('login.html', message = error.args[0])

        return self.render('login.html', message = '')


@route(r'/auth/index/main', '首页')
class IndexMainHandler(CommonBaseHandler):

    '''首页
    '''

    def response(self):
        self.finish()
