import logging
import json
import os
from datetime import datetime
from kafka import KafkaProducer

class EventAggregator:

    def __init__(self, input_sources, output_topic):
        self.logger = logging.getLogger(__name__)
        self.input_sources = input_sources
        self.output_topic = output_topic

        # Create a Kafka producer to send aggregated events
        self.kafka_producer = KafkaProducer(bootstrap_servers='kafka-broker:9092')

    def aggregate_events(self):
        try:
            # Collect events from each input source
            for source in self.input_sources:
                source_events = source.get_events()

                # Aggregate events into a unified format
                aggregated_events = []
                for event in source_events:
                    aggregated_events.append({
                        "timestamp": datetime.utcnow().isoformat(),
                        "type": event['type'],
                        "severity": event['severity'],
                        "description": event['description'],
                        "source": source.name
                    })

                # Send aggregated events to the Kafka topic
                for event in aggregated_events:
                    self.send_event_to_kafka(event)

            self.logger.info('Events aggregated successfully.')
        except Exception as e:
            self.logger.error('Failed to aggregate events:', e)

    def send_event_to_kafka(self, event):
        try:
            # Serialize event data to JSON
            event_json = json.dumps(event).encode('utf-8')

            # Send event to Kafka topic
            self.kafka_producer.send(self.output_topic, event_json)
        except Exception as e:
            self.logger.error(f'Failed to send event to Kafka: {event}', e)

if __name__ == '__main__':
    # Replace with actual input sources and output topic
    input_sources = []
    output_topic = 'aggregated_events'

    # Create an instance of the EventAggregator class
    event_aggregator = EventAggregator(input_sources, output_topic)

    # Start the event aggregation process
    event_aggregator.aggregate_events()
