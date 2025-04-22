class ClientError(Exception):
    """Исключение, возникающее при отсутствии ответа."""
    def __init__(self, message: str = 'Отсутствует ответ'):
        self.message = message
        super().__init__(self.message)
