# This file is part of helipad (http://github.com/jgeewax/helipad).
#
# Copyright (C) 2010 JJ Geewax http://geewax.org/
# All rights reserved.
#
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

# =============================================================================
# Imports
# =============================================================================
from __future__ import with_statement
import inspect
import os
import random
import string
import sys
import time
import mimetypes
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp import blobstore_handlers

# =============================================================================
# Exports
# =============================================================================
__all__ = ['app', 'BlobstoreDownloadHandler', 'BlobstoreUploadHandler',
           'debug', 'find_file', 'Handler', 'json', 'open_file', 'root',
           'static', 'template_root', 'VERSION']

# =============================================================================
# Convenience imports
# =============================================================================
from django.utils import simplejson as json

# =============================================================================
# Private globals
# =============================================================================
_DEBUG = None
_ROOT_MODULE = None
_TEMPLATE_ROOT = None

# =============================================================================
# Public globals
# =============================================================================
VERSION = (0, 1, 2)


# =============================================================================
# Classes
# =============================================================================

class HandlerMixin(object):
  SESSION_COOKIE_NAME = 'session_id'

  def static(self, path):
    file_name = find_file(path)

    # Try to guess the content type:
    file_type, _ = mimetypes.guess_type(file_name)
    if file_type:
      self.response.headers['Content-Type'] = file_type

    # Write the file to the output stream
    with open(file_name, 'r') as f:
      for line in f:
        self.response.out.write(line)

  @classmethod
  def render(cls, path, params=None):
    env = cls._get_template_environment()
    template = env.get_template(path)
    return template.render(params or {})

  def template(self, path, params=None):
    self.response.out.write(self.render(path, params))

  @property
  def session(self):
    key = self.get_cookie(self.SESSION_COOKIE_NAME)
    session = Session(key)

    # If we had to create a new session, set the cookie so it persists
    if not key:
      self.set_cookie(self.SESSION_COOKIE_NAME, session.key)

    return session

  def set_cookie(self, name, value='', path='/'):
    self.response.headers.add_header(
      'Set-Cookie',
      '%s=%s; Path=%s' % (name, value, path),
    )
    self.request.cookies[name] = value

  def get_cookie(self, name):
    return self.request.cookies.get(name)

  def clear_cookie(self, name):
    if name in self.request.cookies:
      del self.request.cookies[name]

    self.set_cookie(name)

  @classmethod
  def _get_template_environment(cls):
    if not template_root():
      raise ValueError("Template root not set.")

    jinja_path = os.path.join(os.path.dirname(__file__), 'jinja2')
    if jinja_path not in sys.path:
      sys.path.insert(0, jinja_path)

    from jinja2 import Environment, FileSystemLoader

    return Environment(loader=FileSystemLoader(
      os.path.join(os.path.dirname(root().__file__), template_root())
    ))


class Handler(HandlerMixin, webapp.RequestHandler):
  pass


class BlobstoreDownloadHandler(HandlerMixin,
  blobstore_handlers.BlobstoreDownloadHandler):
  pass


class BlobstoreUploadHandler(HandlerMixin,
  blobstore_handlers.BlobstoreUploadHandler):
  pass


class Application(object):
  def __init__(self, *args, **kwargs):
    self.url_mapping = self._get_url_mapping(*args, **kwargs)
    self.application = self.get_application(self.url_mapping)
    self.main = self.get_main_method(self.application)

  @classmethod
  def get_application(cls, url_mapping):
    return webapp.WSGIApplication(url_mapping, debug=debug())

  @classmethod
  def get_main_method(cls, application):
    def main():
      from google.appengine.ext.webapp.util import run_wsgi_app
      run_wsgi_app(application)
    return main

  @classmethod
  def _get_url_mapping(cls, *args):
    prefix, mapping = cls._get_prefix_and_mapping(args)

    # If there is just one Handler, bind it to any URL
    if inspect.isclass(mapping) and issubclass(mapping, webapp.RequestHandler):
      return [('.*', mapping)]

    # A dictionary of {'/route/': Handler, ...}
    elif isinstance(mapping, dict):
      return cls._get_url_mapping(prefix, mapping.items())

    # A list of tuples of [('/route/', Handler), ...]
    elif isinstance(mapping, (list, tuple)):
      mappings = list(mapping)
      if prefix:
        for i, item in enumerate(mappings):
          mappings[i] = (prefix + item[0], item[1])
      return mappings

    raise ValueError("Invalid arguments: %s" % args)

  @classmethod
  def _get_prefix_and_mapping(cls, args):
    if len(args) == 1:
      return None, args[0]
    elif len(args) == 2:
      return args

    raise ValueError("Invalid arguments: %s" % args)


class StaticApplication(Application):
  @classmethod
  def _get_url_mapping(cls, *args):
    prefix, mapping = cls._get_prefix_and_mapping(args)

    # If there is just one string, bind it to any URL
    if isinstance(mapping, basestring):
      return [('.*', cls._get_static_handler(mapping))]

    # A dictionary of {'/route/': '/path/to/file.html', ...}
    elif isinstance(mapping, dict):
      return cls._get_url_mapping(prefix, mapping.items())

    # A list of tuples of [('/route/', '/path/to/file.html'), ...]
    elif isinstance(mapping, (list, tuple)):
      mappings = list(mapping)
      for i, item in enumerate(mappings):
        mappings[i] = (item[0], cls._get_static_handler(item[1]))

      return super(StaticApplication, cls)._get_url_mapping(prefix, mappings)

    raise ValueError("Invalid arguments: %s" % args)

  @classmethod
  def _get_static_handler(cls, path):
    class StaticHandler(Handler):
      def get(self):
        self.static(path)
    return StaticHandler


class Session(object):
  _key = None
  cache = memcache

  def __init__(self, session_key=None):
    if not session_key:
      session_key = self.get_random_key()

    self._key = session_key

  @classmethod
  def get_random_key(cls):
    timestamp_string = str(time.time())
    choices = string.letters + string.digits
    random_string = ''.join(random.choice(choices) for _ in xrange(10))
    return random_string + timestamp_string.replace('.', '')

  @property
  def key(self):
    return self._key

  def get(self, key):
    return self.cache.get(key, namespace=self.key)

  def set(self, key, value):
    return self.cache.set(key, value, namespace=self.key)

  def delete(self, key):
    return self.cache.delete(key, namespace=self.key)


# =============================================================================
# Functions
# =============================================================================

def debug(value=None):
  """
  Sets the debug flag for helipad applications.
  """
  global _DEBUG

  if value is None:
    return _DEBUG

  _DEBUG = bool(value)

  # Return a reference to this module
  # This let's us string together method calls.
  return __import__('helipad', globals(), locals(), [], -1)


def root(module=None):
  """
  Sets the "root module" for helipad.

  The root module's directory is used as the definition of where relative paths
  are based off of.
  """
  global _ROOT_MODULE

  if module is None:
    return _ROOT_MODULE

  if isinstance(module, basestring):
    components = module.split('.')
    module = __import__(module, globals(), locals(), [], -1)

    for component in components[1:]:
      module = getattr(module, component)

  if inspect.ismodule(module):
    _ROOT_MODULE = module
  else:
    raise ValueError("Invalid module: %s" % module)

  # Return a reference to this module
  # This let's us string together method calls.
  return __import__('helipad', globals(), locals(), [], -1)


def template_root(directory=None):
  global _TEMPLATE_ROOT

  if directory is None:
    return _TEMPLATE_ROOT

  _TEMPLATE_ROOT = directory

  # Return a reference to this module
  # This let's us string together method calls.
  return __import__('helipad', globals(), locals(), [], -1)


def open_file(path, mode='r'):
  return open(find_file(path), mode)


def find_file(path):
  return os.path.join(os.path.dirname(root().__file__), path)


def app(*args, **kwargs):
  app = Application(*args, **kwargs)
  return app.main, app.application


def static(*args, **kwargs):
  app = StaticApplication(*args, **kwargs)
  return app.main, app.application
