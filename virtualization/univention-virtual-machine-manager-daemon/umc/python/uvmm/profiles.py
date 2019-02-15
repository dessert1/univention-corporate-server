# -*- coding: utf-8 -*-
#
# Univention Management Console
#  module: management of virtualization servers
#
# Copyright 2010-2019 Univention GmbH
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

from univention.admin.uexceptions import base as udm_error
import univention.admin.handlers.uvmm.profile as uvmm_profile

from univention.lib.i18n import Translation

from univention.management.console.log import MODULE
from univention.management.console.ldap import machine_connection

from urlparse import urlsplit

from .tools import object2dict

_ = Translation('univention-management-console-modules-uvmm').translate


class Profile(object):

	"""
	Single UVMM profile.
	"""

	def __init__(self, profile):
		for key, value in profile.items():
			if key not in ('cpus',):
				if value in ('0', 'FALSE'):
					value = False
				elif value in ('1', 'TRUE'):
					value = True
			setattr(self, key, value)


class Profiles(object):

	"""
	UVMM profiles.
	"""

	PROFILE_RDN = 'cn=Profiles,cn=Virtual Machine Manager'
	VIRTTECH_MAPPING = {
		'kvm-hvm': _('Full virtualization (KVM)'),
	}

	@machine_connection(write=False)
	def read_profiles(self, ldap_connection=None, ldap_position=None):
		"""
		Read all profiles from LDAP.
		"""
		base = "%s,%s" % (Profiles.PROFILE_RDN, ldap_position.getDn())
		res = ()
		if ldap_connection is not None:
			try:
				res = uvmm_profile.lookup(
					None,
					ldap_connection,
					'',
					base=base,
					scope='sub',
					required=False,
					unique=False
				)
			except udm_error as exc:
				MODULE.error("Failed to read profiles: %s" % (exc,))
		self.profiles = [(obj.dn, Profile(obj.info)) for obj in res]

	def _filter_profiles(self, node_pd):
		"""
		Return profiles valid for node.
		"""
		uri = urlsplit(node_pd.uri)
		# set default virtualization technology
		tech = 'kvm' if uri.scheme == 'qemu' else uri.scheme
		# read architectures from capabilities
		archs = set([t.arch for t in node_pd.capabilities]) | set(('automatic',))

		return [
			(dn, item)
			for dn, item in self.profiles
			if item.arch in archs and item.virttech.startswith(tech)
		]

	def profile_query(self, request):
		"""
		Returns a list of profiles for the given virtualization technology.
		"""
		self.required_options(request, 'nodeURI')

		def _finished(data):
			"""
			Process asynchronous UVMM NODE_LIST answer.
			"""
			return [
				{'id': dn, 'label': item.name}
				for pd in data
				for (dn, item) in self._filter_profiles(pd)
			]

		self.uvmm.send(
			'NODE_LIST',
			self.process_uvmm_response(request, _finished),
			group='default',
			pattern=request.options['nodeURI']
		)

	def profile_get(self, request):
		"""
		Returns a list of profiles for the given virtualization technology.
		"""
		self.required_options(request, 'profileDN')

		for dn, profile in self.profiles:
			if dn == request.options['profileDN']:
				self.finished(request.id, object2dict(profile))
				return

		self.finished(
			request.id,
			None,
			_('Unknown profile'),
			success=False
		)
