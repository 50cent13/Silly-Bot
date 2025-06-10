
use std::fs;
use serenity::async_trait;
use serenity::model::channel::Message;
use serenity::model::gateway::Ready;
use serenity::prelude::*;

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, ctx: Context, msg: Message) {
        // Ignore bot messages
        if msg.author.bot {
            return;
        }

        // Handle !rust_ping command
        if msg.content == "!rust_ping" {
            let response_msg = format!("Rust bot received ping from {} at {}", msg.author.name, msg.timestamp);
            
            // Write to shared file
            if let Err(e) = fs::write("shared.txt", &response_msg) {
                eprintln!("Failed to write to shared.txt: {}", e);
            }
            
            if let Err(why) = msg.channel_id.say(&ctx.http, "Rust bot ping received! Message written to shared.txt").await {
                println!("Error sending message: {:?}", why);
            }
            
            println!("Rust bot: {}", response_msg);
        }
        
        // Handle !check_python command
        else if msg.content == "!check_python" {
            match fs::read_to_string("shared.txt") {
                Ok(content) => {
                    let response = if content.trim().is_empty() {
                        "Shared file is empty".to_string()
                    } else if content.contains("Python bot") {
                        format!("Message from Python bot: {}", content)
                    } else {
                        format!("Current shared message: {}", content)
                    };
                    
                    if let Err(why) = msg.channel_id.say(&ctx.http, response).await {
                        println!("Error sending message: {:?}", why);
                    }
                },
                Err(_) => {
                    if let Err(why) = msg.channel_id.say(&ctx.http, "Shared file not found").await {
                        println!("Error sending message: {:?}", why);
                    }
                }
            }
        }
    }

    async fn ready(&self, _: Context, ready: Ready) {
        println!("Rust bot logged in as {}", ready.user.name);
    }
}

#[tokio::main]
async fn main() {
    dotenv::dotenv().ok();
    
    let token = std::env::var("BOT_TOKEN_RS")
        .expect("Expected BOT_TOKEN_RS in environment");

    let intents = GatewayIntents::GUILD_MESSAGES
        | GatewayIntents::DIRECT_MESSAGES
        | GatewayIntents::MESSAGE_CONTENT;

    let mut client = Client::builder(&token, intents)
        .event_handler(Handler)
        .await
        .expect("Err creating client");

    if let Err(why) = client.start().await {
        println!("Client error: {:?}", why);
    }
}
