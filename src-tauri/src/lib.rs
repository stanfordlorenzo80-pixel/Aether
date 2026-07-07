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

use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandEvent;

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
        .plugin(tauri_plugin_updater::Builder::new().build())
        .manage(Mutex::new(EngineState {
            port: 8420,
            connected: false,
        }))
        .setup(|app| {
            let window = app.get_webview_window("main");
            if let Some(win) = window {
                info!("Main window created: {:?}", win.title());
            }

            info!("Spawning Python Engine Sidecar...");
            let sidecar_command = app.shell().sidecar("engine").unwrap();
            let (mut rx, _child) = sidecar_command.spawn().expect("Failed to spawn sidecar");

            tauri::async_runtime::spawn(async move {
                while let Some(event) = rx.recv().await {
                    match event {
                        CommandEvent::Stdout(line) => info!("Engine: {}", String::from_utf8_lossy(&line)),
                        CommandEvent::Stderr(line) => info!("Engine Err: {}", String::from_utf8_lossy(&line)),
                        _ => {}
                    }
                }
            });

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
