from django.db import models


class UserMoodle(models.Model):
	deleted = models.BooleanField()
	suspended = models.BooleanField()
	username = models.CharField(max_length=100)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)

	def __unicode__(self):
		return self.username

	class Meta:
		db_table = 'mdl_user'
		managed = False

class Course(models.Model):
	
	category = models.IntegerField(db_column='category')	
	
	def __unicode__(self):
		return str(self.category)

	class Meta:
		db_table = 'mdl_course'
		managed = False



class Role(models.Model):
	name = models.CharField(max_length=255)
	shortname = models.CharField(max_length=100)

	def __unicode__(self):
		return self.shortname

	class Meta:
		db_table = 'mdl_role'
		managed = False

class UserRole(models.Model):
	status = models.IntegerField()
	user = models.ForeignKey('UserMoodle', db_column='userid')
	role = models.ForeignKey('Role', db_column='enrolid')


	class Meta:
		db_table = 'mdl_user_enrolments'
		managed = False

class UserRoleA(models.Model):
	user = models.ForeignKey('UserMoodle', db_column='userid')
	role = models.ForeignKey('Role', db_column='roleid')


	class Meta:
		db_table = 'mdl_role_assignments'
		managed = False
