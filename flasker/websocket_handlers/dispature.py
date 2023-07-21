import re



class Dispature:

    def __init__(self, handlers):
        self.handlers = handlers
        self.message = None

    def consume(self, message):
        try:
#            self.message = self.queue.get(block=True, timeout=2)
            self.message = message
            if self.message and len(self.handlers) > 0:
                for handler in self.handlers:
                    if re.match(handler.role, self.message.get('cmd', ''))\
                            and hasattr(handler, 'apply_handler'):

                        handler.apply_handler(self.message)

        except Exception as e:
            print('no message found')

