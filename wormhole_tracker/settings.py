#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# This file is part of wormhole-tracker package released under
# the GNU GPLv3 license. See the LICENSE file for more information.

from os import urandom
from pkg_resources import resource_filename


settings = {
    'static_path': resource_filename('wormhole_tracker', 'static'),
    'template_path': resource_filename('wormhole_tracker', 'templates'),
    'cookie_secret': urandom(24).encode('base-64').strip(),
    'login_url': '/sign',
    'db_path': '/home/wormhole-tracker/data.db',
}
