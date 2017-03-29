#!#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# This file is part of wormhole-tracker package released under
# the GNU GPLv3 license. See the LICENSE file for more information.

import logging

from tornado.escape import json_encode
from tornado.websocket import WebSocketHandler

from wormhole_tracker.auxiliaries import s


class BaseSocketHandler(WebSocketHandler):
    @property
    def client_id(self):
        return self.application.client_id

    @property
    def client_key(self):
        return self.application.client_key

    @property
    def vagrants(self):
        return self.application.vagrants

    @property
    def state_storage(self):
        return self.application.state_storage

    @property
    def crud(self):
        return self.application.crud

    @property
    def user_id(self):
        return s(self.get_secure_cookie("auth_cookie"))

    @property
    def user(self):
        return self.application.users.get(self.user_id)

    @property
    def authorize(self):
        return self.application.authorize

    @property
    def character(self):
        return self.application.character

    @property
    def spawn(self):
        return self.application.spawn

    async def safe_write(self, message):
        logging.warning(message)
        if self.ws_connection is None:
            logging.error('Connection is already closed.')
        else:
            self.write_message(json_encode(message))
