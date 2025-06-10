
use std::{fs, thread, time::Duration};

fn main() {
    dotenv::dotenv().ok();
    println!("Rust bot started. Watching for shared messages...");

    loop {
        let content = fs::read_to_string("shared.txt").unwrap_or_default();
        if !content.is_empty() {
            println!("Rust bot read message: {}", content);
            
            // Write response back to shared file
            let response = format!("Rust bot processed: {}", content);
            fs::write("shared.txt", response).unwrap_or_else(|e| {
                eprintln!("Failed to write to shared.txt: {}", e);
            });
        }
        thread::sleep(Duration::from_secs(2));
    }
}
