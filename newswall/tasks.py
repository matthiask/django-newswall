# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from django.utils.datetime_safe import datetime
from django.core.management import call_command
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='update_newswall')
def update_newswall():
    logger.info('Newswall update started at {}'.format(datetime.now()))
    call_command('update_newswall')
