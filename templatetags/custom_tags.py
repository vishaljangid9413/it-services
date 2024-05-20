from django import template
register = template.Library()



@register.filter
def apply_tax(cost, tax_percentage):
    try:
        cost = float(cost)
        tax_percentage = float(tax_percentage)
        total_amount = cost + (cost * (tax_percentage / 100))
        return round(total_amount, 2) 
    except Exception as e:
        print(str(e))
        return cost