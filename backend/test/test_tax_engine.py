from ..tax_engine import calculate_tax

def test_basic():
    r = calculate_tax(1000000, 200000)
    assert r["income"] == 1000000
    assert r["deductions"] == 200000
    assert r["taxable_income"] == 800000
    assert "tax" in r
