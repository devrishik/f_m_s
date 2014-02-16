from __future__ import division, absolute_import, unicode_literals
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	phone_number = models.CharField(
        _("Phone number"), max_length=20, blank=True)

	@property
	def name(self):
		return self.get_full_name()

	class Meta:
		verbose_name = _('User')
		verbose_name_plural = _('Users')
