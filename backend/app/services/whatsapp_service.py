import logging

from ..config import Settings

logger = logging.getLogger(__name__)


def send_booking_notification(settings: Settings, reference_number: str, text: str) -> bool:
    if not all((settings.whatsapp_provider, settings.whatsapp_api_key, settings.whatsapp_phone_number_id)):
        logger.info("WhatsApp provider is not configured; notification skipped.")
        return False

    logger.warning(
        "WhatsApp provider credentials are configured, but no provider-specific adapter is enabled for %s.",
        settings.whatsapp_provider,
    )
    return False
