#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-11-07 21:43:17 (CST)
# Last Update:星期二 2017-9-19 12:55:28 (CST)
#          By:
# Description:
# **************************************************************************
import os
import logging
from logging.handlers import SMTPHandler
from logging import Formatter


def init_app(app):
    config = app.config
    logs_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'logs'))
    if not os.path.exists(logs_folder):
        os.mkdir(logs_folder)
    formatter = Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        ''')

    info_log = os.path.join(logs_folder, config['INFO_LOG'])

    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log, maxBytes=100000, backupCount=10)

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(logs_folder, config['ERROR_LOG'])

    error_file_handler = logging.handlers.RotatingFileHandler(
        error_log, maxBytes=100000, backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    if app.config["SEND_LOGS"]:
        from .common.helper import ThreadedSMTPHandler
        credentials = (config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
        mailhost = (config['MAIL_SERVER'], config['MAIL_PORT'])
        mail_handler = ThreadedSMTPHandler(
            secure=(),
            mailhost=mailhost,
            fromaddr=config['MAIL_DEFAULT_SENDER'],
            toaddrs=config['RECEIVER'],
            subject='Your Application Failed',
            credentials=credentials)

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)
