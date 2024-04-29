def take_proffit(price, max_price, buy_price, coef, coef_tp):
    stop_loss_price = get_stop_loss_price(max_price, coef)
    return stop_loss_price if stop_loss_price > price > buy_price * coef_tp else None


def stop_loss(price, buy_price, coef):
    stop_loss_price = get_stop_loss_price(buy_price, coef)
    return stop_loss_price if price < stop_loss_price else None


def get_stop_loss_price(price, coef):
    return price * coef
