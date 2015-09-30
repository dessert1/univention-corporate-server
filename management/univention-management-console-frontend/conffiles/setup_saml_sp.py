#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Univention Management Console
# Univention Configuration Registry Module to rewrite SAML SP configuration for UMC
#
# Copyright 2015 Univention GmbH
#
# http://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <http://www.gnu.org/licenses/>.

import os
from glob import glob
from subprocess import call
from urlparse import urlparse
workaround = set()

def handler(config_registry, changes):
	if not isinstance(changes.get('umc/saml/idp-server'), (list, tuple)):
		# workaround for Bug #39444
		print 'skipping UCR registration'
		return
	if workaround:
		return  # Bug #39443
	workaround.add(True)
	cleanup()
	metadata_download_failed = []
	saml_idp = config_registry.get('umc/saml/idp-server')
	if saml_idp and not download_idp_metadata(saml_idp):
		metadata_download_failed.append(saml_idp)
	reload_webserver()
	if not rewrite_sasl_configuration():
		raise SystemExit('Could not rewrite SASL configuration for UMC.')
	if metadata_download_failed:
		raise SystemExit('Could not download IDP metadata for %s' % (', '.join(metadata_download_failed),))


def cleanup():
	for metadata in glob('/usr/share/univention-management-console/saml/idp/*.xml'):
		os.remove(metadata)


def download_idp_metadata(metadata):
	idp = bytes(urlparse(metadata).netloc)
	filename = '/usr/share/univention-management-console/saml/idp/%s.xml' % (idp,)
	rc = call([
		'/usr/bin/wget',
		'--ca-certificate', '/etc/univention/ssl/ucsCA/CAcert.pem',
		metadata,
		'-O', filename,
	])
	if rc and os.path.exists(filename):
		os.remove(filename)
	return rc == 0


def rewrite_sasl_configuration():
	# rewrite UMC-PAM configuration to include every IDP entry
	rc = call(['/usr/sbin/ucr', 'commit', '/etc/pam.d/univention-management-console'])
	# enable saml sasl module
	rc += call(['/usr/sbin/ucr', 'commit', '/etc/ldap/sasl2/slapd.conf'])
	return rc == 0


def reload_webserver():
	try:
		call(['/etc/init.d/univention-management-console-web-server', 'reload'])
	except (IOError, OSError):
		pass
