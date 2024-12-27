from fastapi import APIRouter, HTTPException
from src.service.verification_service import VerificationService
from jose import jwt, JWTError

router = APIRouter()

SECRET_KEY = ""  # Replace with your actual secret key
ALGORITHM = "HS256"  # Algorithm used for JWT


@router.get("/hackathon/participants/verify")
async def verify_participant(jwt_token: str, service: VerificationService) -> dict[str, str]:
    try:
        # Decode the JWT token
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        participant_id = payload.get("sub")
        is_admin = payload.get("is_admin", None)
        team_id = payload.get("team_id", None)

        # Check if is_admin is False
        if is_admin is None or is_admin is not False:
            raise HTTPException(status_code=400, detail="Invalid token payload for this operation.")

        # Call the service method to verify the participant
        await service.verify_random_participant(participant_id, team_id)

        # Return a success response
        return {"message": "Verification successful, participant is now verified."}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
