import asyncio
from aiokafka import AIOKafkaConsumer

class KafkaConsumer:
    def __init__(self, topic, bootstrap_servers='localhost:9092', group_id="my-group"):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest"
        )
        await self.consumer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume(self):
        try:
            async for msg in self.consumer:
                print(f"Received message: {msg.value.decode('utf-8')}")
        finally:
            await self.stop()

async def main():
    consumer = KafkaConsumer("test_topic")
    await consumer.start()
    await consumer.consume()

if __name__ == "__main__":
    asyncio.run(main())
