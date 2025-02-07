"""
requirements.py

Copyright 2013 Andres Riancho

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
from w3af.core.controllers.dependency_check.pip_dependency import PIPDependency

CORE = 1
GUI = 2

CORE_PIP_PACKAGES = [PIPDependency('clamd', 'clamd', '1.0.1'),
                     PIPDependency('github', 'PyGithub', '1.21.0'),
                     #PIPDependency('git.util', 'GitPython', '0.3.2rc1'),
                     PIPDependency('git.util', 'GitPython', '0.3.2.RC1'),
                     PIPDependency('pybloomfilter', 'pybloomfiltermmap', '0.3.11'),
                     PIPDependency('esmre', 'esmre', '0.3.1'),
                     PIPDependency('phply', 'phply', '0.9.1'),
                     PIPDependency('nltk', 'nltk', '2.0.4'),
                     PIPDependency('chardet', 'chardet', '2.1.1'),
                     PIPDependency('pdfminer', 'pdfminer', '20110515'),
                     PIPDependency('concurrent.futures', 'futures', '2.1.5'),
                     PIPDependency('OpenSSL', 'pyOpenSSL', '0.13.1'),
                     PIPDependency('lxml', 'lxml', '2.3.2'),
                     #PIPDependency('scapy.config', 'scapy-real', '2.2.0.dev0'),
                     PIPDependency('scapy.config', 'scapy-real', '2.2.0-dev'),
                     PIPDependency('guess_language', 'guess-language', '0.2'),
                     PIPDependency('cluster', 'cluster', '1.1.1b3'),
                     PIPDependency('msgpack', 'msgpack-python', '0.2.4'),
                     PIPDependency('ntlm', 'python-ntlm', '1.0.1'),
                     PIPDependency('Halberd', 'halberd', '0.2.4'),
                     PIPDependency('BeautifulSoup', 'BeautifulSoup', '3.2.1'),
                     PIPDependency('darts.lib.utils', 'darts.util.lru', '0.5')]

GUI_PIP_EXTRAS = [PIPDependency('xdot', 'xdot', '0.6'),]

GUI_PIP_PACKAGES = CORE_PIP_PACKAGES[:]
GUI_PIP_PACKAGES.extend(GUI_PIP_EXTRAS)
