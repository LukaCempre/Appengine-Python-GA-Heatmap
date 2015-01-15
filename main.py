#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import os
from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

decorator = OAuth2DecoratorFromClientSecrets(
  os.path.join(os.path.dirname(__file__), 'client_secret.json'),
  'https://www.googleapis.com/auth/analytics.readonly')

service = build('calendar', 'v3')

class MainHandler(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):
		self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
