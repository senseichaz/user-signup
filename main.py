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
import re

class Index(webapp2.RequestHandler):
    """
    Handles requests coming into "/" root
    """



    def get(self):

        error_username = self.request.get("error_username")
        error_password = self.request.get("error_password")
        error_verify = self.request.get("error_verify")
        error_email = self.request.get("error_email")

        username = self.request.get("username")
        email = self.request.get("email")

        html = """
        <form action="/welcome" method="post">
        <h2> Signup </h2>
        Username <input type="text" name="username" value="{0}"><font color="red">   """.format(username) + error_username + """</font> <br> <br>
        Password <input type="text" name="password"><font color="red">   """ + error_password + """</font> <br> <br>
        Verify Password <input type="text" name="verify"><font color="red">   """ + error_verify + """</font> <br> <br>
        Email (optional) <input type="text" name="email" value="{0}"><font color="red">   """.format(email) + error_email + """</font> <br>

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

        # RE methods

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASS_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        def valid_email(email):
            return USER_RE.match(email)


        # if the user typed nothing at all, redirect and yell at them
        if (username.strip() == ""):
            error_username = "Nothin from nothin leaves nothin, you've gotta have somethin"
            self.redirect("/?error_username=" + cgi.escape(error_username, quote=True))
        elif USER_RE.match(username) == None:
            error_username = "Testing my patience here buddy"
            self.redirect("/?error_username=" + cgi.escape(error_username, quote=True))
        elif " " in username:
            error_username = "No spaces, doofus"
            self.redirect("/?error_username=" + cgi.escape(error_username, quote=True))
        elif password == "":
            error_password = "Nothin from nothin..."
            self.redirect("/?error_password=" + cgi.escape(error_password, quote=True) + "&username=" + cgi.escape(username, quote=True) + "&email=" + cgi.escape(email, quote=True))
        elif password != verify or PASS_RE.match(password) == None:
            error_password = "What's your malfunction brother, can't type?"
            self.redirect("/?error_password=" + cgi.escape(error_password, quote=True) + "&username=" + cgi.escape(username, quote=True) + "&email=" + cgi.escape(email, quote=True))
        elif EMAIL_RE.match(email) == None and email != "":
            error_email = "You're killing me here dude"
            self.redirect("/?error_email=" + cgi.escape(error_email, quote=True) + "&username=" + cgi.escape(username, quote=True) + "&email=" + cgi.escape(email, quote=True))

        # write output
        self.response.out.write("<strong> Welcome, " + username + "  </strong>")



app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
