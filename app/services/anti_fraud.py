import asyncio
import logging
from decimal import Decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_fraud(amount: Decimal) -> bool:
    logger.info(f"Anti-Fraud analysis for the amount {amount}")
    await asyncio.sleep(2)
    is_fraud = amount > Decimal("50000.00")
    if is_fraud:
        logger.warning("Anti-Fraud: Suspicious transaction has been detected and blocked")
    return is_fraud