"""Модульные тесты для калькулятора комиссий."""

import pytest

from calculator import calculate_commission


class TestCalculateCommission:
    """Позитивные тесты: корректный расчёт для каждого диапазона."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (100, 50.0),
            (1000, 50.0),
            (1001, 100.0),
            (20000, 100.0),
            (20001, 400.01),
            (40000, 600.0),
        ],
    )
    def test_commission_calculation(self, amount, expected):
        assert calculate_commission(amount) == pytest.approx(expected)


class TestNewFixedFeeRule:
    """Тесты новой функциональности: > 40 000 → фикс. 500 руб."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (40001, 500.0),
            (45000, 500.0),
            (50000, 500.0),
        ],
    )
    def test_fixed_fee_over_40k(self, amount, expected):
        assert calculate_commission(amount) == pytest.approx(expected)

    def test_boundary_40000_uses_old_rule(self):
        """40 000 — ещё по старому правилу: 200 + 1% = 600."""
        assert calculate_commission(40000) == pytest.approx(600.0)

    def test_boundary_40001_uses_new_rule(self):
        """40 001 — уже новое правило: фикс. 500."""
        assert calculate_commission(40001) == pytest.approx(500.0)


class TestCalculateCommissionErrors:
    """Негативные тесты: обработка невалидных данных."""

    @pytest.mark.parametrize("invalid_amount", [99, 50001, -1, 0, 100000])
    def test_amount_out_of_range_raises_value_error(self, invalid_amount):
        with pytest.raises(ValueError):
            calculate_commission(invalid_amount)

    @pytest.mark.parametrize("invalid_amount", ["abc", None, [100], {"a": 1}])
    def test_non_numeric_amount_raises_type_error(self, invalid_amount):
        with pytest.raises(TypeError):
            calculate_commission(invalid_amount)


class TestBoundaryValues:
    """Граничные значения всех диапазонов."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (100, 50.0),
            (1000, 50.0),
            (1001, 100.0),
            (20000, 100.0),
            (20001, 400.01),
            (40000, 600.0),
            (40001, 500.0),
            (50000, 500.0),
        ],
    )
    def test_boundaries(self, amount, expected):
        assert calculate_commission(amount) == pytest.approx(expected)

    def test_float_amount_accepted(self):
        """Дробная сумма тоже допустима."""
        assert calculate_commission(100.5) == pytest.approx(50.0)