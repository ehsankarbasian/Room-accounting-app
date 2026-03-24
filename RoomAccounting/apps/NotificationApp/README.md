# NotificationApp

A pluggable Django notification framework that cleanly separates message definition, channel selection, and delivery.

`NotificationApp` helps large Django projects keep notification logic out of business code while supporting multiple delivery channels and easily extensible message types.

---

## Features

- Multi‑channel notification delivery
- Pluggable sender architecture
- Message type registry
- Channel prioritization and fallback
- Transport‑agnostic message definitions
- Clean separation between domain logic and delivery infrastructure

---

## Installation

Install the package (example if published to PyPI):

```bash
pip install django-notification-app
```

Add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "apps.NotificationApp.apps.NotificationAppConfig",

    # Optional example implementations
    "apps.NotificationContribApp.apps.NotificationContribAppConfig",
]
```

Run migrations:

```bash
python manage.py migrate
```

---

## Quick Start

### 1. Create a verified channel

```python
from apps.NotificationApp.models import NotificationChannel
from apps.NotificationContribApp.notification_types import SenderType

NotificationChannel.objects.create(
    user=user,
    channel_type=SenderType.EMAIL,
    identifier="user@example.com",
    is_verified=True,
    is_primary=True,
)
```

### 2. Send a notification

Using a domain service:

```python
from apps.NotificationContribApp.services.auth_notifications import AuthNotifications

AuthNotifications.send_otp(user=user, code="482913")
```

Or call the dispatcher directly:

```python
from apps.NotificationApp.dispatching import NotificationDispatcher
from apps.NotificationContribApp.messages import OtpMessage
from apps.NotificationContribApp.notification_types import MessageType

NotificationDispatcher.send(
    user=user,
    message_type=MessageType.OTP,
    data=OtpMessage.Data(code="482913"),
)
```

---

## Architecture Overview

The system follows a simple pipeline:

```
Application → Dispatcher → Message Mapper → Channel Resolver → Sender
```

Flow:

1. Your application requests a notification.
2. The message definition maps domain data to a canonical message.
3. The dispatcher selects the best verified channel.
4. The corresponding sender delivers the message.

This design keeps domain logic independent from delivery mechanisms.

---

## Core Concepts

### NotificationChannel

Represents a user's delivery endpoint.

Key fields:

- `channel_type` – sender key such as `email` or `sms`
- `identifier` – destination value (email, phone, chat id, etc.)
- `is_verified` – only verified channels are used
- `is_primary` – preferred channel
- `priority` – lower value means higher priority

---

### NotificationDispatcher

Primary entry point for sending notifications.

```python
NotificationDispatcher.send(
    user,
    message_type,
    data,
    channel_override=None,
    preferred_channels=None,
)
```

Responsibilities:

- validate message data
- resolve the best delivery channel
- map domain data to canonical message format
- call the appropriate sender

---

### Registries

The framework uses two registries:

- **MessageRegistry** – maps message types to message definitions
- **SenderRegistry** – maps channel types to sender implementations

This enables a plugin‑style architecture where new messages or channels can be added without modifying core code.

---

## Usage Examples

### Prefer certain channels

```python
from apps.NotificationContribApp.notification_types import SenderType

NotificationDispatcher.send(
    user=user,
    message_type=MessageType.OTP,
    data=OtpMessage.Data(code="482913"),
    preferred_channels=[SenderType.BALE, SenderType.EMAIL],
)
```

### Force a specific channel

```python
NotificationDispatcher.send(
    user=user,
    message_type=MessageType.OTP,
    data=OtpMessage.Data(code="482913"),
    channel_override=SenderType.EMAIL,
)
```

### Handle missing channels

```python
from apps.NotificationApp.dispatching.errors import NoAvailableChannelError

try:
    NotificationDispatcher.send(
        user=user,
        message_type=MessageType.OTP,
        data=OtpMessage.Data(code="482913"),
    )
except NoAvailableChannelError:
    pass
```

---

## Extending the App

### Add a new sender

```python
from enum import StrEnum

from apps.NotificationApp.interfaces import MessageSenderInterface
from apps.NotificationApp.registry import SenderRegistry


class SenderType(StrEnum):
    PUSH = "push"


@SenderRegistry.register(SenderType.PUSH)
class PushSender(MessageSenderInterface):

    @staticmethod
    def render_payload(message):
        return {"body": message.text}

    @staticmethod
    def send_payload(identifier, payload):
        pass
```

---

### Add a new message type

```python
from dataclasses import dataclass
from enum import StrEnum

from apps.NotificationApp.interfaces.message_base import MessageDefinitionInterface
from apps.NotificationApp.interfaces.message_mapper import MessageMapperInterface
from apps.NotificationApp.registry import MessageRegistry
from apps.NotificationContribApp.message_schema import CanonicalMessage


class MessageType(StrEnum):
    INVOICE_READY = "invoice_ready"


@MessageRegistry.register(MessageType.INVOICE_READY)
class InvoiceReadyMessage(MessageDefinitionInterface):

    @dataclass
    class Data:
        invoice_number: str

    class Mapper(MessageMapperInterface):

        @staticmethod
        def map(data):
            return CanonicalMessage(text=f"Invoice {data.invoice_number} is ready")
```

---

### Auto‑register modules

If you build your own extension app:

```python
from django.apps import AppConfig


class BillingNotificationAppConfig(AppConfig):
    name = "apps.BillingNotificationApp"

    def ready(self):
        from apps.NotificationApp.registry.autodiscover import autodiscover_modules

        autodiscover_modules("apps.BillingNotificationApp.messages")
        autodiscover_modules("apps.BillingNotificationApp.senders")
```

---

## Supported Channels

Typical sender implementations may include:

- Email
- SMS
- Chat bots (e.g. Bale / Telegram)
- Push notifications

Additional channels can be added through custom sender classes.

---

## Settings

### Django Email Settings

Example settings used by email senders:

- `DEFAULT_FROM_EMAIL`
- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`

### Example Custom Sender Settings

Example for a Bale bot sender:

- `BALE_BOT_TOKEN`

---

## Design Goals

- Decouple message definition from delivery logic
- Keep domain logic independent from infrastructure
- Allow adding channels without modifying existing code
- Encourage service‑layer notification triggering

---

## Best Practices

- Wrap dispatcher usage inside domain services
- Keep messages transport‑agnostic
- Use verified channels only
- Prefer `preferred_channels` for delivery rules
- Use `channel_override` only when necessary

---

## Project Structure

```
apps/NotificationApp/
  admin.py
  apps.py
  models.py
  dispatching/
  interfaces/
  registry/
  scaffolding/
```

Example extension package:

```
apps/NotificationContribApp/
  apps.py
  notification_types.py
  message_schema/
  messages/
  senders/
  services/
```

---

## Contributing

Contributions are welcome. When extending the system:

- implement new delivery channels via sender classes
- define new notification types via message definitions
- keep message mapping separate from transport logic

For project‑specific behavior, prefer creating a separate extension app instead of modifying the core library.