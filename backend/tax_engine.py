def calculate_tax(income: float, deductions: float):
    # sanitize
    income = float(max(income, 0))
    deductions = float(max(deductions, 0))
    taxable = max(income - deductions, 0)

    # Example progressive rates — replace with official formulas
    tax = 0.0
    remaining = taxable
    brackets = [
        (300000, 0.07),
        (300000, 0.11),
        (float("inf"), 0.15)
    ]
    for limit, rate in brackets:
        part = min(remaining, limit)
        tax += part * rate
        remaining -= part
        if remaining <= 0:
            break

    return {"income": income, "deductions": deductions, "taxable_income": taxable, "tax": round(tax, 2)}
