from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from montecarlo.services.auth import require_auth
from montecarlo.services.web import ConfigRequestJson
import montecarlo.helpers as jh

router = APIRouter(prefix="/config", tags=["Configuration"], dependencies=[Depends(require_auth)])


@router.post("/get")
def get_config(json_request: ConfigRequestJson):
    """
    Get the current configuration
    """

    from montecarlo.modes.data_provider import get_config as gc

    return JSONResponse({
        'data': gc(json_request.current_config, has_live=jh.has_live_trade_plugin())
    }, status_code=200)


@router.post("/update")
def update_config(json_request: ConfigRequestJson):
    """
    Update the configuration
    """

    from montecarlo.modes.data_provider import update_config as uc

    uc(json_request.current_config)

    return JSONResponse({'message': 'Updated configurations successfully'}, status_code=200)
