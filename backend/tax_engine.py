def calculate_tax(income: float, deductions: float) -> dict:
    taxable_income = max(income - deductions, 0)

    # Example progressive rate (replace with real rules)
    if taxable_income <= 300000:
        tax = taxable_income * 0.07
    elif taxable_income <= 600000:
        tax = 300000 * 0.07 + (taxable_income - 300000) * 0.11
    else:
        tax = 300000 * 0.07 + 300000 * 0.11 + (taxable_income - 600000) * 0.15

    return {
        "taxable_income": taxable_income,
        "tax": tax
    }

