import asyncio
from aiokafka import AIOKafkaProducer

class KafkaProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send(self, topic, value):
        if not self.producer:
            raise RuntimeError("Producer not started")
        await self.producer.send_and_wait(topic, value.encode('utf-8'))

async def main():
    producer = KafkaProducer()
    await producer.start()
    try:
        await producer.send("test_topic", "Hello Kafka")
        print("Message sent")
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(main())
