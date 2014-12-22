class MoodleRouter(object):

  def db_for_read(self, model, **hints):
    if model._meta.app_label == 'moodle':
      return 'moodle'
    return None
