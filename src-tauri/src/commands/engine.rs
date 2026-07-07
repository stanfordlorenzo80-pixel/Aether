use std::sync::Mutex;
use std::time::Duration;

use log::{info, warn};
use reqwest::Client;

use crate::models::{EngineHealth, EngineStatus};
use crate::EngineState;

/// Shared HTTP client configuration: 2-second timeout, no redirects.
fn http_client() -> Result<Client, String> {
    Client::builder()
        .timeout(Duration::from_secs(2))
        .redirect(reqwest::redirect::Policy::none())
        .build()
        .map_err(|e| format!("failed to build HTTP client: {e}"))
}

/// Probe the engine's `/health` endpoint.
///
/// Returns an `EngineHealth` payload on success, or a structured
/// offline response when the engine is unreachable.
#[tauri::command]
pub async fn check_engine_health(
    state: tauri::State<'_, Mutex<EngineState>>,
) -> Result<EngineHealth, String> {
    let port = {
        let guard = state
            .lock()
            .map_err(|e| format!("state lock poisoned: {e}"))?;
        guard.port
    };

    let url = format!("http://localhost:{port}/health");
    info!("checking engine health at {url}");

    let client = http_client()?;

    match client.get(&url).send().await {
        Ok(resp) => {
            if !resp.status().is_success() {
                let status_code = resp.status().as_u16();
                warn!("engine returned HTTP {status_code}");
                return Ok(EngineHealth {
                    status: "error".to_string(),
                    version: String::new(),
                    uptime: 0.0,
                    providers: Vec::new(),
                });
            }

            let health: EngineHealth = resp
                .json()
                .await
                .map_err(|e| format!("failed to parse health response: {e}"))?;

            // Update shared state.
            if let Ok(mut guard) = state.lock() {
                guard.connected = health.status == "healthy";
            }

            info!("engine reports status={}", health.status);
            Ok(health)
        }
        Err(e) => {
            warn!("engine unreachable: {e}");

            if let Ok(mut guard) = state.lock() {
                guard.connected = false;
            }

            Ok(EngineHealth {
                status: "offline".to_string(),
                version: String::new(),
                uptime: 0.0,
                providers: Vec::new(),
            })
        }
    }
}

/// Fetch extended status from the engine's `/api/status` endpoint.
///
/// Falls back to a sensible offline payload when the engine is down
/// instead of surfacing raw connection errors to the frontend.
#[tauri::command]
pub async fn get_engine_status(
    state: tauri::State<'_, Mutex<EngineState>>,
) -> Result<EngineStatus, String> {
    let port = {
        let guard = state
            .lock()
            .map_err(|e| format!("state lock poisoned: {e}"))?;
        guard.port
    };

    let url = format!("http://localhost:{port}/api/status");
    info!("fetching engine status from {url}");

    let client = http_client()?;

    match client.get(&url).send().await {
        Ok(resp) => {
            if !resp.status().is_success() {
                let code = resp.status().as_u16();
                warn!("engine status endpoint returned HTTP {code}");
                return Ok(EngineStatus {
                    status: "error".to_string(),
                    version: String::new(),
                    uptime: 0.0,
                    active_connections: 0,
                    loaded_providers: Vec::new(),
                });
            }

            let status: EngineStatus = resp
                .json()
                .await
                .map_err(|e| format!("failed to parse status response: {e}"))?;

            if let Ok(mut guard) = state.lock() {
                guard.connected = status.status == "running";
            }

            info!("engine status: {}", status.status);
            Ok(status)
        }
        Err(e) => {
            warn!("engine status unreachable: {e}");

            if let Ok(mut guard) = state.lock() {
                guard.connected = false;
            }

            Ok(EngineStatus {
                status: "offline".to_string(),
                version: String::new(),
                uptime: 0.0,
                active_connections: 0,
                loaded_providers: Vec::new(),
            })
        }
    }
}
