use log::{info, warn};
use tauri_plugin_store::StoreExt;

use crate::models::AppSettings;

/// The filename used by `tauri-plugin-store` for persisted settings.
const STORE_PATH: &str = "settings.json";

/// The key under which the entire settings object is stored.
const SETTINGS_KEY: &str = "app_settings";

/// Load application settings from the persistent store.
///
/// Returns the saved `AppSettings` if found, or `AppSettings::default()`
/// on first launch or if the stored value is corrupt.
#[tauri::command]
pub fn get_settings(app: tauri::AppHandle) -> Result<AppSettings, String> {
    info!("loading settings from store");

    let store = app
        .store(STORE_PATH)
        .map_err(|e| format!("failed to open store: {e}"))?;

    match store.get(SETTINGS_KEY) {
        Some(value) => {
            let settings: AppSettings = serde_json::from_value(value.clone()).unwrap_or_else(|e| {
                warn!("stored settings are corrupt ({e}), returning defaults");
                AppSettings::default()
            });
            info!(
                "settings loaded — provider={}, model={}",
                settings.default_provider, settings.default_model
            );
            Ok(settings)
        }
        None => {
            info!("no saved settings found, returning defaults");
            Ok(AppSettings::default())
        }
    }
}

/// Persist application settings to the store.
///
/// Serialises the entire `AppSettings` struct under a single key
/// and flushes to disk.
#[tauri::command]
pub fn save_settings(app: tauri::AppHandle, settings: AppSettings) -> Result<(), String> {
    info!(
        "saving settings — provider={}, model={}, port={}",
        settings.default_provider, settings.default_model, settings.engine_port
    );

    let store = app
        .store(STORE_PATH)
        .map_err(|e| format!("failed to open store: {e}"))?;

    let value = serde_json::to_value(&settings)
        .map_err(|e| format!("failed to serialise settings: {e}"))?;

    store.set(SETTINGS_KEY.to_string(), value);

    store
        .save()
        .map_err(|e| format!("failed to flush store to disk: {e}"))?;

    info!("settings persisted to {STORE_PATH}");
    Ok(())
}
