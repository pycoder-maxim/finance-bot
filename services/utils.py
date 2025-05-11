def format_currency(amount: float) -> str:
    """Форматирует сумму в виде 1 234.56 руб"""
    return f"{amount:,.2f} руб".replace(",", " ")

def is_valid_float(text: str) -> bool:
    """Проверка, можно ли преобразовать строку в число"""
    try:
        float(text.strip())
        return True
    except ValueError:
        return False