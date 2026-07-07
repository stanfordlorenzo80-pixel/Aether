use std::sync::Mutex;
use std::time::Duration;

use log::{info, warn};
use reqwest::Client;

use crate::models::{ConnectionTestResult, ProviderInfo};
use crate::EngineState;

/// Shared HTTP client — mirrors the one in `engine.rs`.
fn http_client() -> Result<Client, String> {
    Client::builder()
        .timeout(Duration::from_secs(2))
        .redirect(reqwest::redirect::Policy::none())
        .build()
        .map_err(|e| format!("failed to build HTTP client: {e}"))
}

/// List all registered model providers from the engine.
///
/// Calls `GET /api/models/providers` and returns a `Vec<ProviderInfo>`.
/// Returns an empty list when the engine is unreachable.
#[tauri::command]
pub async fn list_providers(
    state: tauri::State<'_, Mutex<EngineState>>,
) -> Result<Vec<ProviderInfo>, String> {
    let port = {
        let guard = state
            .lock()
            .map_err(|e| format!("state lock poisoned: {e}"))?;
        guard.port
    };

    let url = format!("http://localhost:{port}/api/models/providers");
    info!("listing providers via {url}");

    let client = http_client()?;

    match client.get(&url).send().await {
        Ok(resp) => {
            if !resp.status().is_success() {
                let code = resp.status().as_u16();
                warn!("providers endpoint returned HTTP {code}");
                return Err(format!("engine returned HTTP {code}"));
            }

            let providers: Vec<ProviderInfo> = resp
                .json()
                .await
                .map_err(|e| format!("failed to parse providers response: {e}"))?;

            info!("received {} provider(s)", providers.len());
            Ok(providers)
        }
        Err(e) => {
            warn!("could not reach providers endpoint: {e}");
            Ok(Vec::new())
        }
    }
}

/// Run a connectivity test against a single provider.
///
/// Calls `POST /api/models/test/{provider_id}` and returns a
/// `ConnectionTestResult` with latency and any error message.
#[tauri::command]
pub async fn test_provider_connection(
    state: tauri::State<'_, Mutex<EngineState>>,
    provider_id: String,
) -> Result<ConnectionTestResult, String> {
    let port = {
        let guard = state
            .lock()
            .map_err(|e| format!("state lock poisoned: {e}"))?;
        guard.port
    };

    let url = format!("http://localhost:{port}/api/models/test/{provider_id}");
    info!("testing provider '{provider_id}' via {url}");

    let client = http_client()?;

    match client.post(&url).send().await {
        Ok(resp) => {
            if !resp.status().is_success() {
                let code = resp.status().as_u16();
                warn!("provider test returned HTTP {code}");
                return Ok(ConnectionTestResult {
                    connected: false,
                    latency_ms: 0.0,
                    error: Some(format!("engine returned HTTP {code}")),
                });
            }

            let result: ConnectionTestResult = resp
                .json()
                .await
                .map_err(|e| format!("failed to parse test result: {e}"))?;

            info!(
                "provider '{provider_id}' connected={} latency={}ms",
                result.connected, result.latency_ms
            );
            Ok(result)
        }
        Err(e) => {
            warn!("provider test failed for '{provider_id}': {e}");
            Ok(ConnectionTestResult {
                connected: false,
                latency_ms: 0.0,
                error: Some(format!("engine unreachable: {e}")),
            })
        }
    }
}
