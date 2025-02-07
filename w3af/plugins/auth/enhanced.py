"""
enhanced.py

Copyright 2011 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
from splinter import Browser
import urllib2
import inspect
import w3af.core.controllers.output_manager as om

from w3af.core.controllers.plugins.auth_plugin import AuthPlugin
from w3af.core.controllers.exceptions import BaseFrameworkException

from w3af.core.data.options.opt_factory import opt_factory
from w3af.core.data.options.option_list import OptionList

from lxml.html import parse, tostring
from urllib2 import urlopen
class enhanced(AuthPlugin):
    """Enhanced authentication plugin."""
    
    def __init__(self,options=[]):
        AuthPlugin.__init__(self)
        self.extras = [] # In (name,value,type) format. Actually holds all parameters (username, password included)
        self.data_format = ""
        self.check_url = 'http://example.com/home'
        self.check_string = ''
        
        self.method = "POST"
        self.options = []
        self.auth_url = 'https://example.com/login'
    def _run_auth_sequence(self):
        """
        Scrape form values from authentication URL
        """
        try:
            request = urllib2.Request(self.auth_url)
            response = None
            try:
                
                #Zero out any previous extras configurations
                self.extras = []
                #Checker for Beautiful Soup, deprecated
                #ck_value = lambda d, i: d.get(key) if d.get(key) != None else ''
                
                # Sanity check for lxml
                ck_value = lambda d: d if d != None else ''
                doc = parse(urlopen(self.auth_url)).getroot()
                for form in doc.forms:
                    om.out.debug("Found form")
                    
                    # Find all inputs, including those with no value field
                    for input_key in form.inputs.keys():
                        self.extras.append( (input_key, ck_value(form.fields[input_key]) ) )
                    """
                    For now break after parsing first form
                    TODO: Add option to select form
                    """
                    break
                self._update_data_format()
            except urllib2.HTTPError as e:
                print e
                om.out.debug("Error fetching login URL: %s" % e)
            except urllib2.URLError as u:
                print u
                om.out.debug("URL Error: ",u)
            except Exception as ex:
                print ex
                om.out.debug("Unknown Error: ",ex)
        except (RuntimeError, ), e:
            raise e
    def _update_data_format(self):
        """
        Update the self.data_format options to reflect form values.
        """
        format_name = 'a'
        format_value = 'A'
        for i in range(0,len(self.extras)-1):
            #Add a format placeholder for each extra parameter. Add '&' if not last parameter
            self.data_format += "%%%s=%%%s%s" %  (format_name,format_value,'&' if i<len(self.extras)-2 else '',)
            #get next letter for next extra parameter
            format_name = chr(ord(format_name)+1)
            format_value = chr(ord(format_value)+1)
        # Update the data_format value in options by swapping
        self.get_options()
        new_format_option = list(self.options[1])
        new_format_option[1] = self.data_format
        new_format_option = tuple(new_format_option)
        self.options[1] = new_format_option
    def login(self):
        """
        Login to the application.
        """

        msg = 'Logging into the application using %s/%s' % (self.username,
                                                            self.password)
        om.out.debug(msg)

        data = self._get_data_from_format()

        try:
            functor = getattr(self._uri_opener, self.method)
            functor(self.auth_url, data)

            if not self.is_logged():
                raise Exception("Can't login into web application as %s/%s"
                                % (self.username, self.password))
            else:
                om.out.debug('Login success for %s/%s' % (
                    self.username, self.password))
                return True
        except Exception, e:
            if self._login_error:
                om.out.error(str(e))
                self._login_error = False
            return False

    def _get_data_from_format(self):
        """
        :return: A string with all the information to send to the login URL.
        This string contains the username, password, and all the other information
        that was provided by the user and needs to be transmitted to the remote
        web application.
        """
        result = self.data_format
        
        
        format_name = 'a'
        format_value = 'A'
        for extra in self.extras:
            result.replace("%%%s" % format_name, extra[0])
            result.replace("%%%s" % format_value, extra[1])
            format_name = chr(ord(format_name)+1)
            format_value = chr(ord(format_value)+1)
        return result

    def logout(self):
        """User login."""
        return None

    def is_logged(self):
        """Check user session."""
        
        try:
            body = self._uri_opener.GET(self.check_url, grep=False).body
            logged_in = self.check_string in body

            msg_yes = 'User "%s" is currently logged into the application'
            msg_no = 'User "%s" is NOT logged into the application'
            msg = msg_yes if logged_in else msg_no
            om.out.debug(msg % self.username)

            return logged_in
        except Exception:
            return False
        
        return False
    def get_options(self):
        """
        :return: A list of option objects for this plugin.
        """
        self.options = [
            ('auth_url', self.auth_url, 'string',
             'URL to begin the authentication sequence from'),
            ('check_url', self.check_url, 'url',
             'URL used to verify if the session is still active by looking for'
             ' the check_string.'),
            ('check_string', self.check_string, 'string',
             'String for searching on check_url page to determine if the'
             'current session is active.')
                ]
        for extra in self.extras:
            #Add another option
            option = (extra[0], extra[1],'string',"Form field")
            self.options.append(option)
        
        ol = OptionList()
        for o in self.options:
            ol.add(opt_factory(o[0], o[1], o[3], o[2], help=o[3]))
        options = self.options
        return ol

    def set_options(self, options_list):
        """
        This method sets all the options that are configured using
        the user interface generated by the framework using
        the result of get_options().

        :param options_list: A dict with the options for the plugin.
        :return: No value is returned.
        """
        
        curr_auth_url = options_list['auth_url'].get_value()
        if curr_auth_url != self.auth_url:
            self.auth_url = curr_auth_url
            #Do not run if empty auth_url
            if self.auth_url != "":
                self._run_auth_sequence()
            
        self.data_format = options_list['data_format'].get_value()
        self.check_url = options_list["check_url"].get_value()
        self.check_string = options_list['check_string'].get_value()
    def get_long_desc(self):
        """
        :return: A DETAILED description of the plugin functions and features.
        """
        return """
        This authentication plugin can login to applications where more than just username and password
        are required (e.g. CSRF nonce, other hidden fields). To see an example, try configuring a scan
        for a website with hidden form fields.

        A potentially unlimited number of configurable parameters exist.
        Fill the parameter "auth_url". Click Save to run the form scraper and update the options.
        -> Data is formatted like so: %param_a=%PARAM_A&%param_b=%PARAM_B ... etc
        """
