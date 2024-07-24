class VanillaCAParser:
    def __init__(self) -> None:
        pass

    def parse_order_date_text(self, text):
        text = text.replace(',', '')
        return text.replace(' ', '_')
    
    def parse_order_number_text(self, text):
        return text