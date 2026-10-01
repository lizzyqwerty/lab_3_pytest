"""Модуль «Калькулятор комиссий» для денежных переводов."""

# --- Границы суммы перевода ---
MIN_AMOUNT = 100
MAX_AMOUNT = 50_000

# --- Границы тарифных диапазонов ---
LOW_THRESHOLD = 1_000
MID_THRESHOLD = 20_000
HIGH_FIXED_THRESHOLD = 40_000

# --- Размеры комиссий ---
LOW_FEE = 50.0
MID_FEE = 100.0
HIGH_BASE_FEE = 200.0
HIGH_EXTRA_RATE = 0.01
VERY_HIGH_FIXED_FEE = 500.0


def _validate_amount(amount) -> None:
    """Проверяет корректность суммы перевода."""
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError("Сумма перевода должна быть числом")

    if amount < MIN_AMOUNT or amount > MAX_AMOUNT:
        raise ValueError(
            f"Сумма перевода должна быть от {MIN_AMOUNT} до {MAX_AMOUNT} руб."
        )


def calculate_commission(amount: int) -> float:
    """
    Рассчитывает комиссию для денежного перевода.

    Тарифные правила:
        * от 100 до 1 000 руб. включительно — 50 руб.;
        * от 1 001 до 20 000 руб. включительно — 100 руб.;
        * от 20 001 до 40 000 руб. включительно — 200 руб. + 1% от суммы;
        * свыше 40 000 руб. — фиксированные 500 руб.

    Args:
        amount (int): Сумма перевода (от 100 до 50 000 руб.)

    Returns:
        float: Размер комиссии

    Raises:
        ValueError: Если сумма не входит в допустимый диапазон
        TypeError: Если передан нечисловой тип
    """
    _validate_amount(amount)

    if amount <= LOW_THRESHOLD:
        return LOW_FEE
    if amount <= MID_THRESHOLD:
        return MID_FEE
    if amount <= HIGH_FIXED_THRESHOLD:
        return HIGH_BASE_FEE + amount * HIGH_EXTRA_RATE
    return VERY_HIGH_FIXED_FEE