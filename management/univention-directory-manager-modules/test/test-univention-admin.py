#!/usr/bin/python2.7
#
# Copyright 2017 Univention GmbH
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

from univention.admin import property
import unittest
from argparse import Namespace as N


class FakeObject(dict):
	set_defaults = True


class TestProperty(unittest.TestCase):

	def test_default_sv(self):
		p = property()
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), '')

	def test_default_mv(self):
		p = property(multivalue=True)
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), [])

	def test_base_default_sv(self):
		p = property()
		o = FakeObject()
		self.assertIsNone(p.default(o))

	def test_base_default_mv(self):
		p = property(multivalue=True)
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_str_default_sv(self):
		p = property(default='x')
		o = FakeObject()
		self.assertEqual(p.default(o), 'x')

	# def test_str_default_mv(self):
	# 	p = property(multivalue=True, default=('x', 'y'))
	# 	o = N(set_defaults=True)
	# 	self.assertEqual(p.default(o), ['x', 'y'])

	def test_complex_syntax(self):
		s = N(subsyntaxes=())
		p = property(multivalue=False, default=(('x', 'y'),), syntax=s)
		o = FakeObject()
		self.assertEqual(p.default(o), ('x', 'y'))

	def test_template_sv_empty(self):
		p = property(multivalue=False, default=('templ', ['prop']))
		o = FakeObject(prop='')
		self.assertIsNone(p.default(o))

	def test_template_sv_set(self):
		p = property(multivalue=False, default=('<prop>', ['prop']))
		o = FakeObject(prop='value')
		self.assertEqual(p.default(o), 'value')

	def test_template_mv_set(self):
		p = property(multivalue=True, default=('<prop1>', '<prop2>'))
		o = FakeObject(prop1='value1', prop2='value2')
		self.assertEqual(p.default(o), ['value1', 'value2'])

	def test_template_mv_incomplete(self):
		p = property(multivalue=True, default=('<prop>', None))
		o = FakeObject()
		self.assertEqual(p.default(o), ['<prop>'])

	def test_template_mv_empty(self):
		p = property(multivalue=True, default=('', None))
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_callable_set(self):
		x = object()
		o = FakeObject(prop='value1')
		f = lambda obj, extra: 'value2' if extra is x and obj is o else 'error'
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), 'value2')

	def test_callable_empty_sv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertIsNone(p.default(o))

	def test_callable_empty_mv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=True, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), [])

	def test_fallback_sv(self):
		o = FakeObject()
		p = property(multivalue=False, default=(None,))
		self.assertIsNone(p.default(o))

	def test_fallback_mv(self):
		o = FakeObject()
		p = property(multivalue=True, default=(None,))
		self.assertEqual(p.default(o), [])


if __name__ == '__main__':
	unittest.main()
#!/usr/bin/python2.7

from univention.admin import property
import unittest
from argparse import Namespace as N


class FakeObject(dict):
	set_defaults = True


class TestProperty(unittest.TestCase):

	def test_default_sv(self):
		p = property()
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), '')

	def test_default_mv(self):
		p = property(multivalue=True)
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), [])

	def test_base_default_sv(self):
		p = property()
		o = FakeObject()
		self.assertIsNone(p.default(o))

	def test_base_default_mv(self):
		p = property(multivalue=True)
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_str_default_sv(self):
		p = property(default='x')
		o = FakeObject()
		self.assertEqual(p.default(o), 'x')

	# def test_str_default_mv(self):
	# 	p = property(multivalue=True, default=('x', 'y'))
	# 	o = N(set_defaults=True)
	# 	self.assertEqual(p.default(o), ['x', 'y'])

	def test_complex_syntax(self):
		s = N(subsyntaxes=())
		p = property(multivalue=False, default=(('x', 'y'),), syntax=s)
		o = FakeObject()
		self.assertEqual(p.default(o), ('x', 'y'))

	def test_template_sv_empty(self):
		p = property(multivalue=False, default=('templ', ['prop']))
		o = FakeObject(prop='')
		self.assertIsNone(p.default(o))

	def test_template_sv_set(self):
		p = property(multivalue=False, default=('<prop>', ['prop']))
		o = FakeObject(prop='value')
		self.assertEqual(p.default(o), 'value')

	def test_template_mv_set(self):
		p = property(multivalue=True, default=('<prop1>', '<prop2>'))
		o = FakeObject(prop1='value1', prop2='value2')
		self.assertEqual(p.default(o), ['value1', 'value2'])

	def test_template_mv_incomplete(self):
		p = property(multivalue=True, default=('<prop>', None))
		o = FakeObject()
		self.assertEqual(p.default(o), ['<prop>'])

	def test_template_mv_empty(self):
		p = property(multivalue=True, default=('', None))
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_callable_set(self):
		x = object()
		o = FakeObject(prop='value1')
		f = lambda obj, extra: 'value2' if extra is x and obj is o else 'error'
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), 'value2')

	def test_callable_empty_sv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertIsNone(p.default(o))

	def test_callable_empty_mv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=True, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), [])

	def test_fallback_sv(self):
		o = FakeObject()
		p = property(multivalue=False, default=(None,))
		self.assertIsNone(p.default(o))

	def test_fallback_mv(self):
		o = FakeObject()
		p = property(multivalue=True, default=(None,))
		self.assertEqual(p.default(o), [])


if __name__ == '__main__':
	unittest.main()
#!/usr/bin/python2.7
#
# Copyright 2017 Univention GmbH
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

from univention.admin import property
import unittest
from argparse import Namespace as N


class FakeObject(dict):
	set_defaults = True


class TestProperty(unittest.TestCase):

	def test_default_sv(self):
		p = property()
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), '')

	def test_default_mv(self):
		p = property(multivalue=True)
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), [])

	def test_base_default_sv(self):
		p = property()
		o = FakeObject()
		self.assertIsNone(p.default(o))

	def test_base_default_mv(self):
		p = property(multivalue=True)
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_str_default_sv(self):
		p = property(default='x')
		o = FakeObject()
		self.assertEqual(p.default(o), 'x')

	# def test_str_default_mv(self):
	# 	p = property(multivalue=True, default=('x', 'y'))
	# 	o = N(set_defaults=True)
	# 	self.assertEqual(p.default(o), ['x', 'y'])

	def test_complex_syntax(self):
		s = N(subsyntaxes=())
		p = property(multivalue=False, default=(('x', 'y'),), syntax=s)
		o = FakeObject()
		self.assertEqual(p.default(o), ('x', 'y'))

	def test_template_sv_empty(self):
		p = property(multivalue=False, default=('templ', ['prop']))
		o = FakeObject(prop='')
		self.assertIsNone(p.default(o))

	def test_template_sv_set(self):
		p = property(multivalue=False, default=('<prop>', ['prop']))
		o = FakeObject(prop='value')
		self.assertEqual(p.default(o), 'value')

	def test_template_mv_set(self):
		p = property(multivalue=True, default=('<prop1>', '<prop2>'))
		o = FakeObject(prop1='value1', prop2='value2')
		self.assertEqual(p.default(o), ['value1', 'value2'])

	def test_template_mv_incomplete(self):
		p = property(multivalue=True, default=('<prop>', None))
		o = FakeObject()
		self.assertEqual(p.default(o), ['<prop>'])

	def test_template_mv_empty(self):
		p = property(multivalue=True, default=('', None))
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_callable_set(self):
		x = object()
		o = FakeObject(prop='value1')
		f = lambda obj, extra: 'value2' if extra is x and obj is o else 'error'
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), 'value2')

	def test_callable_empty_sv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertIsNone(p.default(o))

	def test_callable_empty_mv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=True, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), [])

	def test_fallback_sv(self):
		o = FakeObject()
		p = property(multivalue=False, default=(None,))
		self.assertIsNone(p.default(o))

	def test_fallback_mv(self):
		o = FakeObject()
		p = property(multivalue=True, default=(None,))
		self.assertEqual(p.default(o), [])


if __name__ == '__main__':
	unittest.main()
#!/usr/bin/python2.7

from univention.admin import property
import unittest
from argparse import Namespace as N


class FakeObject(dict):
	set_defaults = True


class TestProperty(unittest.TestCase):

	def test_default_sv(self):
		p = property()
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), '')

	def test_default_mv(self):
		p = property(multivalue=True)
		o = N(set_defaults=False)
		self.assertEqual(p.default(o), [])

	def test_base_default_sv(self):
		p = property()
		o = FakeObject()
		self.assertIsNone(p.default(o))

	def test_base_default_mv(self):
		p = property(multivalue=True)
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_str_default_sv(self):
		p = property(default='x')
		o = FakeObject()
		self.assertEqual(p.default(o), 'x')

	# def test_str_default_mv(self):
	# 	p = property(multivalue=True, default=('x', 'y'))
	# 	o = N(set_defaults=True)
	# 	self.assertEqual(p.default(o), ['x', 'y'])

	def test_complex_syntax(self):
		s = N(subsyntaxes=())
		p = property(multivalue=False, default=(('x', 'y'),), syntax=s)
		o = FakeObject()
		self.assertEqual(p.default(o), ('x', 'y'))

	def test_template_sv_empty(self):
		p = property(multivalue=False, default=('templ', ['prop']))
		o = FakeObject(prop='')
		self.assertIsNone(p.default(o))

	def test_template_sv_set(self):
		p = property(multivalue=False, default=('<prop>', ['prop']))
		o = FakeObject(prop='value')
		self.assertEqual(p.default(o), 'value')

	def test_template_mv_set(self):
		p = property(multivalue=True, default=('<prop1>', '<prop2>'))
		o = FakeObject(prop1='value1', prop2='value2')
		self.assertEqual(p.default(o), ['value1', 'value2'])

	def test_template_mv_incomplete(self):
		p = property(multivalue=True, default=('<prop>', None))
		o = FakeObject()
		self.assertEqual(p.default(o), ['<prop>'])

	def test_template_mv_empty(self):
		p = property(multivalue=True, default=('', None))
		o = FakeObject()
		self.assertEqual(p.default(o), [])

	def test_callable_set(self):
		x = object()
		o = FakeObject(prop='value1')
		f = lambda obj, extra: 'value2' if extra is x and obj is o else 'error'
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), 'value2')

	def test_callable_empty_sv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=False, default=(f, ['prop'], x))
		self.assertIsNone(p.default(o))

	def test_callable_empty_mv(self):
		x = object()
		o = FakeObject(prop='')
		f = lambda obj, extra: 1 / 0
		p = property(multivalue=True, default=(f, ['prop'], x))
		self.assertEqual(p.default(o), [])

	def test_fallback_sv(self):
		o = FakeObject()
		p = property(multivalue=False, default=(None,))
		self.assertIsNone(p.default(o))

	def test_fallback_mv(self):
		o = FakeObject()
		p = property(multivalue=True, default=(None,))
		self.assertEqual(p.default(o), [])


if __name__ == '__main__':
	unittest.main()
