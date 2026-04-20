package event

import (
	"context"
	"encoding/json"
	"errors"
	"log"

	"github.com/cloudevents/sdk-go/v2/event"
	cloudeventprovider "github.com/eclipse-xfsc/cloud-event-provider"
)

type CloudEventPubClient struct {
	ctx    context.Context
	topic  string
	client *cloudeventprovider.CloudEventProviderClient
}

func (c CloudEventPubClient) Close() error {
	return c.client.Close()
}

func (c CloudEventPubClient) Publish(subject string, payload []byte) interface{} {
	data, err := json.Marshal(payload)
	if err != nil {
		log.Fatal(err)
	}
	event, err := cloudeventprovider.NewEvent("event", "test", data)
	if err != nil {
		log.Fatal(err)
	}

	return c.client.PubCtx(c.ctx, event)
}

func NewNatsPubClient(ctx context.Context, topic string, natsURL string) (*CloudEventPubClient, error) {
	client, err := cloudeventprovider.New(cloudeventprovider.Config{
		Protocol: cloudeventprovider.ProtocolTypeNats,
		Settings: cloudeventprovider.NatsConfig{
			Url: natsURL,
		},
	}, cloudeventprovider.ConnectionTypePub, topic)
	if err != nil {
		return nil, errors.New("Could not create cloud event provider client")
	}
	return &CloudEventPubClient{ctx, topic, client}, nil
}

type CloudEventSubClient struct {
	ctx    context.Context
	topic  string
	client *cloudeventprovider.CloudEventProviderClient
}

func (c CloudEventSubClient) Close() error {
	return c.client.Close()
}

func (c CloudEventSubClient) Subscribe(f func(evt event.Event)) error {
	return c.client.SubCtx(c.ctx, f)
}

func NewNatsSubClient(ctx context.Context, topic string, natsURL string) (*CloudEventSubClient, error) {
	client, err := cloudeventprovider.New(cloudeventprovider.Config{
		Protocol: cloudeventprovider.ProtocolTypeNats,
		Settings: cloudeventprovider.NatsConfig{
			Url: natsURL,
		},
	}, cloudeventprovider.ConnectionTypeSub, topic)
	if err != nil {
		return nil, errors.New("Could not create cloud event provider client")
	}
	return &CloudEventSubClient{ctx, topic, client}, nil
}
