# -*- coding: utf-8 -*-
#
# This file is part of wormhole-tracker package released under
# the GNU GPLv3 license. See the LICENSE file for more information.

import logging
from datetime import datetime
from urllib.parse import urlencode, quote

from tornado.options import options

from wormhole_tracker.auxiliaries import a, token_gen
from wormhole_tracker.handlers.base_request import BaseHandler


class SigninHandler(BaseHandler):
    async def get(self):
        """
        Triggers when user pushes "LOG IN with EVE Online" button at /sign;
        Redirects user to app's authorization page at EVE Online site;
        After providing credentials there, user being redirected to our /auth.
        """
        login_eveonline = "https://login.eveonline.com/oauth/authorize/?"

        # Generate state token and store it in the `state_storage`, this
        # way we will accept only our redirected users (CSRF protection)
        state = await token_gen()
        self.state_storage[state] = datetime.now()

        query = urlencode({
            'response_type': 'code',
            'redirect_uri': '%s/auth/' % options.redirect_uri,
            'client_id': self.client_id,
            'scope': 'characterBookmarksRead characterLocationRead',
            #'scope': 'characterLocationRead',
            'state': state,
        })
        login_eveonline += query
        self.redirect(login_eveonline)


class AuthHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        """
        Triggers when EVE Online site redirects user back here, after providing
        credentials there. EVE provides us with "code" and "state" arguments;
        We need "code" to get user info, while "state" is needed for optional
        security purposes, which are not implemented yet.
        """
        state = a(self.get_argument("state"))
        # Check if `state` was generated by our app
        state_registered = self.state_storage.pop(state, None)
        if state_registered:
            logging.info("Time elapsed since signin: %s" % (
                datetime.now() - state_registered)
            )
            code = self.get_argument("code")
            # user_id serves as key to the
            # user object from all handlers
            user_id = await self.authorize(code)
            if user_id:
                self.set_secure_cookie("auth_cookie", user_id)
            self.redirect('/')
        else:
            # Restrict access if not.
            self.set_status(403)
            self.redirect('/watchalookin')


class SignoutHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.clear_cookie("auth_cookie")
        self.redirect('/sign')
