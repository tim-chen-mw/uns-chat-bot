from starlette.requests import Request
from fastapi import APIRouter, Response
from ..services import datasimulator
import json
from ..util import settings

router = APIRouter()

@router.get("/api/updateuns/{area}")
async def input(request: Request, area: str):
    """Endpoint that triggers a UNS update via MQTT
    """
    if area == "packaging":
        simulated_data = datasimulator.generate_packaging_data()
    elif area == "topping_and_freezing":
        simulated_data = datasimulator.generate_topping_and_freezing_data()
    elif area == "dough_prep":
        simulated_data = datasimulator.generate_dough_prep_data()
    
    request.app.mainservice.update_uns(simulated_data)

@router.post("/api/delete_conversation/{conversation_id}")
async def delete_conversation(conversation_id:str, request:Request):
    """Endpoint that deletes a conversation from the coversation manager"""
    response = request.app.mainservice.delete_conversation(conversation_id)
    response_dict = {'delete_success':response}
    return json.dumps(response_dict)
