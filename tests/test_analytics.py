from analytics import Inventory

def test_expired_count():

    inv=Inventory("data/my_actual_alseer_portfolio.csv")
    assert inv.metrics['expired_count'] > 0