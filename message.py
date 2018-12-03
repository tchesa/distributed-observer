
from pickle import dumps

class Message:
  header = ''
  body = any

  def __init__(self, head, body):
    self.header = head
    self.body = body

  def __str__(self):
    return '{}: {}'.format(self.header, self.body)

  def encode(self):
    return dumps(self)
