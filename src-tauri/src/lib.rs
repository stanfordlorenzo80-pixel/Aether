use log::info;
use std::sync::Mutex;
use tauri::Manager;

mod commands;
mod models;

/// Shared application state tracking the Python engine process.
/// Managed via `tauri::State<Mutex<EngineState>>` in command handlers.
pub struct EngineState {
    /// Port the Python engine listens on.
    pub port: u16,
    /// Whether the last health check succeeded.
    pub connected: bool,
}

/// Primary entry point for the Tauri application.
///
/// Initialises logging, registers all plugins and command handlers,
/// manages the shared `EngineState`, and starts the event loop.
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info"))
        .format_timestamp_millis()
        .init();

    info!("Aether v{} starting up", env!("CARGO_PKG_VERSION"));

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_store::Builder::default().build())
        .plugin(tauri_plugin_fs::init())
        .manage(Mutex::new(EngineState {
            port: 8420,
            connected: false,
        }))
        .setup(|app| {
            let window = app.get_webview_window("main");
            if let Some(win) = window {
                info!("Main window created: {:?}", win.title());
            }

            info!("Aether setup complete — engine expected on port 8420");
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            commands::engine::check_engine_health,
            commands::engine::get_engine_status,
            commands::models::list_providers,
            commands::models::test_provider_connection,
            commands::settings::get_settings,
            commands::settings::save_settings,
        ])
        .run(tauri::generate_context!())
        .expect("fatal: failed to start Aether");
}
