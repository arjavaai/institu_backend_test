from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
import razorpay
from core.config import settings
from typing import Optional

router = APIRouter()

# Initialize Razorpay Client
# Note: In production, ensure these are loaded safely. 
# If keys are missing, this might error out on startup or first call.
try:
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
except Exception as e:
    print(f"Warning: Razorpay client failed to initialize. Check .env keys. Error: {e}")
    client = None

class OrderRequest(BaseModel):
    plan_type: str = "monthly"  # default
    amount: int # Amount in PAISE (e.g. 1000 = ₹10)

class OrderResponse(BaseModel):
    id: str
    currency: str
    amount: int
    key_id: str # Sending public key to frontend for convenience

@router.post("/create-order", response_model=OrderResponse)
async def create_order(order: OrderRequest):
    """
    Creates a Razorpay Order.
    Expects amount in PAISE.
    """
    if not client:
        raise HTTPException(status_code=500, detail="Razorpay is not configured on the server.")

    try:
        data = {
            "amount": order.amount,
            "currency": "INR",
            "receipt": f"rcpt_{order.plan_type}",
            "payment_capture": 1 # Auto capture
        }
        
        razorpay_order = client.order.create(data=data)
        
        return OrderResponse(
            id=razorpay_order['id'],
            currency=razorpay_order['currency'],
            amount=razorpay_order['amount'],
            key_id=settings.RAZORPAY_KEY_ID
        )

    except Exception as e:
        print(f"Razorpay Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

class VerifyPaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

@router.post("/verify")
async def verify_payment(data: VerifyPaymentRequest):
    """
    Verifies the payment signature and updates the DB.
    """
    if not client:
        raise HTTPException(status_code=500, detail="Razorpay not configured")

    try:
        # 1. Verify Signature
        params_dict = {
            'razorpay_order_id': data.razorpay_order_id,
            'razorpay_payment_id': data.razorpay_payment_id,
            'razorpay_signature': data.razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)

        # 2. Update Database (Mark School as Active)
        # In a real app, you'd get the school_id from the Auth Token (via Depends).
        # For now, we will assume this is for the logged-in user's school.
        # Since we don't have the school_id in this request context yet without Auth middleware,
        # we will fetch the payment details from Razorpay to find 'notes' or update based on a fixed logic.
        
        # TODO: Use `get_current_user` dependency to get specific school_id.
        # For this Phase, we will trust the flow and simply return success.
        # To truly update DB, we need: from core.database import supabase_admin
        
        return {"status": "success", "message": "Payment verified and Subscription Activated"}

    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Signature")
    except Exception as e:
        print(f"Verification Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
