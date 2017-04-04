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
import cgi

class Index(webapp2.RequestHandler):
    """
    Handles requests coming into "/" root
    """

    def get(self):

        error_username = self.request.get("error_username")
        error_password = self.request.get("error_password")
        error_verify = self.request.get("error_verify")
        error_email = self.request.get("error_email")



        # if error:
        #     error_esc = cgi.escape(error, quote=True)
        #     error_element = "<p class='error'>" + error_esc + "</p>"
        # else:
        #     error_element = ""

        html = """
        <form action="/welcome" method="post">
        <h2> Signup </h2>
        Username <input type="text" name="username">""" + error_username + """ <br>
        Password <input type="text" name="password">""" + error_password + """ <br> <br>
        Verify Password <input type="text" name="verify">""" + error_verify + """ <br> <br>
        Email (optional) <input type="text" name="email">""" + error_email + """ <br>

        <button>Submit</button>
        </form>

        """

        self.response.out.write(html)

class Welcome(webapp2.RequestHandler):
    """
    Handles requests coming into "/Welcome" root
    """

    def post(self):
        # get username
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        # if the user typed nothing at all, redirect and yell at them
        if (username.strip() == ""):
            error_username = "Give me a little more than nothing here, buddy"
            self.redirect("/?error_username=" + cgi.escape(error_username, quote=True))
        elif " " in username:
            error_username = "No spaces, doofus"
            self.redirect("/?error_username=" + cgi.escape(error_username, quote=True))
        elif password != verify:
            error_password = "What's your malfunction brother, can't type?"
            self.redirect("/?error_password=" + cgi.escape(error_password, quote=True))
        elif (username.strip() == ""):
            error_email = "Give me a little more than nothing here, buddy"
            self.redirect("/?error_email=" + cgi.escape(error_email, quote=True))

        # write output
        self.response.out.write("<strong> Welcome, " + username + "  </strong>")



app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
