import os
import warnings
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from montecarlo.services.web import fastapi_app
import montecarlo.helpers as jh
from montecarlo.services.auth import InvalidAuthError, unauthorized_response


@fastapi_app.exception_handler(InvalidAuthError)
async def invalid_auth_exception_handler(_request, _exc):
    return unauthorized_response()


# Suppress pandas deprecation noise in application logs.
warnings.simplefilter(action='ignore', category=FutureWarning)

# get the jesse directory
MONTECARLO_DIR = os.path.dirname(os.path.abspath(__file__))

# define lifespan (replaces deprecated @on_event("shutdown"))
@asynccontextmanager
async def lifespan(app):
    from montecarlo.services import research_jobs
    research_jobs.accept_jobs()
    yield
    from montecarlo.services.db import database
    database.close_connection()
    from montecarlo.services.lsp import terminate_lsp_server
    terminate_lsp_server()
    # Research scripts and analysis jobs run in their own process groups, so they do not
    # receive the terminal's Ctrl+C; stop them explicitly, refusing any job a request was still
    # preparing (research_jobs.shutdown).
    research_jobs.shutdown()

fastapi_app.router.lifespan_context = lifespan

# load homepage
@fastapi_app.get("/")
async def index():
    return FileResponse(f"{MONTECARLO_DIR}/static/index.html")






# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Routes
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
from montecarlo.controllers.websocket_controller import router as websocket_router
from montecarlo.controllers.optimization_controller import router as optimization_router
from montecarlo.controllers.monte_carlo_controller import router as monte_carlo_router
from montecarlo.controllers.exchange_controller import router as exchange_router
from montecarlo.controllers.backtest_controller import router as backtest_router
from montecarlo.controllers.significance_test_controller import router as significance_test_router
from montecarlo.controllers.candles_controller import export_router as candles_export_router, router as candles_router
from montecarlo.controllers.strategy_controller import router as strategy_router
from montecarlo.controllers.auth_controller import router as auth_router
from montecarlo.controllers.config_controller import router as config_router
from montecarlo.controllers.notification_controller import router as notification_router
from montecarlo.controllers.system_controller import router as system_router
from montecarlo.controllers.file_controller import router as file_router
from montecarlo.controllers.lsp_controller import router as lsp_router
from montecarlo.controllers.closed_trade_controller import router as closed_trade_router
from montecarlo.controllers.order_controller import router as order_router
from montecarlo.controllers.tabs_controller import router as tabs_router
from montecarlo.controllers.period_templates_controller import router as period_templates_router
from montecarlo.controllers.route_templates_controller import router as route_templates_router
from montecarlo.controllers.ai_model_controller import router as ai_model_router
from montecarlo.controllers.data_provider_credentials_controller import router as data_provider_credentials_router
from montecarlo.controllers.mcp_controller import router as mcp_router
from montecarlo.controllers.project_files_controller import router as project_files_router
from montecarlo.controllers.research_scripts_controller import router as research_scripts_router
from montecarlo.controllers.session_results_controller import router as session_results_router
from montecarlo.controllers.analysis_controller import router as analysis_router
from montecarlo.services.env import is_test_env

# register routers
fastapi_app.include_router(websocket_router)
fastapi_app.include_router(optimization_router)
fastapi_app.include_router(monte_carlo_router)
fastapi_app.include_router(exchange_router)
fastapi_app.include_router(backtest_router)
fastapi_app.include_router(significance_test_router)
fastapi_app.include_router(candles_router)
fastapi_app.include_router(candles_export_router)
fastapi_app.include_router(strategy_router)
fastapi_app.include_router(auth_router)
fastapi_app.include_router(config_router)
fastapi_app.include_router(notification_router)
fastapi_app.include_router(system_router)
fastapi_app.include_router(file_router)
fastapi_app.include_router(lsp_router)
fastapi_app.include_router(closed_trade_router)
fastapi_app.include_router(order_router)
fastapi_app.include_router(tabs_router)
fastapi_app.include_router(period_templates_router)
fastapi_app.include_router(route_templates_router)
fastapi_app.include_router(ai_model_router)
fastapi_app.include_router(data_provider_credentials_router)
fastapi_app.include_router(mcp_router)
fastapi_app.include_router(project_files_router)
fastapi_app.include_router(research_scripts_router)
fastapi_app.include_router(session_results_router)
fastapi_app.include_router(analysis_router)

if is_test_env():
    from montecarlo.controllers.e2e_controller import router as e2e_router
    fastapi_app.include_router(e2e_router)

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Live Trade Plugin
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
if jh.has_live_trade_plugin():
    from montecarlo.controllers.live_controller import router as live_router
    fastapi_app.include_router(live_router)


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Static Files (Must be loaded at the end to prevent overlapping with API endpoints)
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
fastapi_app.mount("/", StaticFiles(directory=f"{MONTECARLO_DIR}/static"), name="static")
