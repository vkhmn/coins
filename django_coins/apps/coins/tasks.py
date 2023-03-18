from apps.coins.models import Coin, Seller
from apps.coins.services import CoinsCollect
from apps.core.models import Status, CoinUser, Filter
from apps.coins.telegram import send_message

from config.settings.dev import logger


def collect():
    query_set = Filter.objects.select_related('user')
    coins = []
    for fltr in query_set:
        unc_pattern = fltr.user.unc_pattern if fltr.is_unc else None
        coins_collection = CoinsCollect(
            fltr.category.id,
            fltr.pattern,
            unc_pattern,
        )

        try:
            coins_collection.parse_coins()
        except Exception as e:
            logger.error(e)
            continue

        for coin in coins_collection:
            coin['seller'], _ = Seller.objects.get_or_create(
                name=coin.get('seller')
            )
            coins.append(
                (coin, fltr.user)
            )
    for coin, user in coins:
        coin, _ = Coin.objects.get_or_create(**coin)
        CoinUser.objects.get_or_create(
            coin=coin,
            user=user
        )
    return 'Done', len(coins)


def send_messages():
    coins = CoinUser.objects.select_related('user', 'coin').filter(
        status=Status.NEW
    )
    for coin in coins:
        if coin.user.chat_id is None:
            continue

        message_id = send_message(
            chat_id=coin.user.chat_id,
            message=coin.coin.to_msg(),
            image=coin.coin.image,
        )
        if message_id is not None:
            coin.status = Status.SEND
            coin.message_id = message_id
            coin.save()
