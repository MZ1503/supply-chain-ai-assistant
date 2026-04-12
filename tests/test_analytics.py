from analytics import Inventory

def test_expired_count():

    inv=Inventory("data/my_actual_alseer_portfolio.csv")
    assert inv.metrics['expired_count'] > 0

def test_urgent_brands():
    inv = Inventory("data/my_actual_alseer_portfolio.csv")
    assert len(inv.metrics['urgent_brands']) > 0

def test_total_inventory_value():
    inv = Inventory("data/my_actual_alseer_portfolio.csv")
    assert inv.metrics['total_inv_val'] > 0