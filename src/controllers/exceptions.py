class ChannelExistedException(BaseException):
    def __init__(self, channel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = channel


class ChannelNotExistException(BaseException):
    def __init__(self, channel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = channel
