

class MessageHandler:

    def __init__(self, kiosk_manager):
        self.role = None
        self.kiosk_manager = kiosk_manager
        self.ws_manager = kiosk_manager.ws_manager
        self.config = kiosk_manager.config
        self.kiosk_fsm = kiosk_manager.kiosk_fsm
        self.input_blocks = []
        self.output_blocks = []

    def apply_handler(self, message):
        NotImplemented


