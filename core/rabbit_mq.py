import orjson
from aio_pika import Message, ExchangeType
from core.wrappers import try_exc_regular, try_exc_async


@try_exc_async
async def publish_message(connection, message, routing_key, exchange_name, queue_name):
    channel = await connection.channel()
    exchange = await channel.declare_exchange(exchange_name, type=ExchangeType.DIRECT, durable=True)

    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange, routing_key=routing_key)

    message_body = orjson.dumps(message)
    message = Message(message_body)

    await exchange.publish(message, routing_key=routing_key)
    await channel.close()

    return True
