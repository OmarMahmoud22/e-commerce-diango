def cart_id_(request):
    cart = request.session.session_key
    if not cart:
        cart =request.session.create()
    return cart  