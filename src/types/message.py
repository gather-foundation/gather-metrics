class Message:
    def __init__(self, category: str, text: str) -> None:
        self.category: str = category
        self.text: str = text

    def __repr__(self) -> str:
        return f"Message(category='{self.category}', text='{self.text}')"
