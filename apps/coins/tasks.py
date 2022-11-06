from apps.coins.models import Coin, Category, Seller
from config.celery import app
from apps.coins.services import CoinsCollect
from apps.core.models import User, Status, CoinUser
from apps.coins.telegram import send_message


@app.task
def coins_collect():
    collect()
    send_messages()
    return 'GOOD'


def collect():
    query_set = User.objects.prefetch_related('filters')
    coins = []
    for user in query_set:
        coins_collection = CoinsCollect()
        for params in user.filters.all():
            category = params.category
            pattern = params.pattern
            coins_collection.init(category.id, pattern)
            coins_collection.parse_coins()
        for coin in coins_collection:
            coin['seller'], _ = Seller.objects.get_or_create(
                name=coin.get('seller')
            )
            coins.append(
                (coin, user)
            )

    for coin, user in coins:
        coin, _ = Coin.objects.get_or_create(**coin)
        CoinUser.objects.get_or_create(
            coin=coin,
            user=user
        )


def send_messages():
    coins = CoinUser.objects.select_related('user', 'coin').filter(
        status=Status.NEW
    )
    for coin in coins:
        message_id = send_message(
            chat_id=coin.user.chat_id,
            message=coin.coin.to_msg(),
            image=coin.coin.image,
        )
        if message_id is not None:
            coin.status = Status.SEND
            coin.message_id = message_id
            coin.save()
