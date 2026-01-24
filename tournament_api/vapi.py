# from vapi_python import Vapi
from vapi import Vapi
import os

class VapiCall:
    
    def __init__(self) -> None:
        self.client = Vapi(token=os.getenv("VAPI_KEY"))
        self.ALEX = os.getenv("ALEX_MODEL_KEY")
        self.caller = os.getenv("CALLER_KEY")
        self.twillio = os.getenv("TWILLIO_KEY")
        self.clientNumber = os.getenv("CLIENT_NUMBER")

    def reportException(self, error: Exception, assistant_overrides=None):
        # Extract error details
        error_name = error.get("name") if isinstance(error, dict) else getattr(error, "name", None)
        error_message = error.get("message") if isinstance(error, dict) else getattr(error, "msg", None) or getattr(error, "message", None)
        error_type = error.get("type") if isinstance(error, dict) else type(error).__name__
        error_details = str(error)


        
        # Build formatted error context text
        error_context_text = f"\n\nError occurred:\n- Type: {error_type}"
        if error_name:
            error_context_text += f"\n- Name: {error_name}"
        if error_message:
            error_context_text += f"\n- Message: {error_message}"
        error_context_text += f"\n- Details: {error_details}"
        
        # Initialize assistant_overrides if not provided
        assistant_overrides = {
            "firstMessage": "",
            "variableValues": {
                    "error": error_name or error_type,
                    "error_code": 500,
                    "error_message": error_message or error_details,
                    "error_type": error_type,
                    "error_details": error_details
            }
        }
        
        call = self.client.calls.create(
            assistant_id=self.ALEX, 
            customer={"number": self.clientNumber},
            phone_number_id=self.twillio,
            assistant_overrides=assistant_overrides)

        import pdb; pdb.set_trace()

        return call

    def close(self):
        self.vapi.stop()


    
        