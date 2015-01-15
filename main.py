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
import httplib2

decorator = OAuth2DecoratorFromClientSecrets(
  os.path.join(os.path.dirname(__file__), 'client_secret.json'),
  'https://www.googleapis.com/auth/analytics.readonly')

service = build('analytics', 'v3')

class MainHandler(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):
		http = decorator.http()

		report = service.data().ga().get(
		  ids='ga:%s'%self.request.get("viewId"),
		  metrics='ga:sessions',
		  dimensions='ga:hour,ga:dayOfWeek',
		  start_date='2014-12-01',
		  end_date='2014-12-07').execute(http)

		cleanedData = []
		for row in report['rows']:
			rowDictionary = {"day":int(row[1])+1, "hour":int(row[0]) + 1, "value":int(row[2])}
			cleanedData.append(rowDictionary)

		self.response.write(cleanedData)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)


