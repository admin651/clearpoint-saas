from fastapi import APIRouter, Depends, HTTPException, Request
from ..config import settings
from ..auth import get_current_user
import stripe

router = APIRouter(prefix="/billing", tags=["billing"])

def stripe_enabled() -> bool:
    return bool(settings.stripe_secret_key and settings.stripe_public_key)

@router.get("/config")
def config():
    return {
        "enabled": stripe_enabled(),
        "public_key": settings.stripe_public_key,
        "price_ids": {
            "starter": settings.stripe_price_id_starter,
            "growth": settings.stripe_price_id_growth
        }
    }

@router.post("/checkout")
def checkout(plan: str, user = Depends(get_current_user)):
    if not stripe_enabled():
        raise HTTPException(status_code=400, detail="Stripe not configured")
    stripe.api_key = settings.stripe_secret_key
    price_id = settings.stripe_price_id_growth if plan == "growth" else settings.stripe_price_id_starter
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{settings.base_url}/?success=true",
        cancel_url=f"{settings.base_url}/?canceled=true"
    )
    return {"checkout_url": session.url}

@router.post("/webhook")
async def webhook(request: Request):
    # Stub: validate signature if settings.stripe_webhook_secret is set
    payload = await request.body()
    # TODO: verify event, handle subscription status, etc.
    return {"received": True}
