
use std::env;
use std::fs;
use std::sync::Arc;
use serenity::async_trait;
use serenity::model::channel::Message;
use serenity::model::gateway::Ready;
use serenity::prelude::*;
use dotenv::dotenv;

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, ctx: Context, msg: Message) {
        // Check for ping command
        if msg.content == "!rust_ping" {
            // Write to shared file for Python bot to read
            let shared_data = format!("Rust bot received ping from {}", msg.author.name);
            if let Err(e) = fs::write("shared.txt", &shared_data) {
                eprintln!("Error writing to shared.txt: {}", e);
            }

            if let Err(why) = msg.channel_id.say(&ctx.http, "Rust bot pong! Message sent to Python bot.").await {
                println!("Error sending message: {:?}", why);
            }
        }

        // Check for messages from Python bot (via file)
        if msg.content == "!check_python" {
            match fs::read_to_string("shared.txt") {
                Ok(content) => {
                    if content.contains("Python bot received a ping command!") {
                        if let Err(why) = msg.channel_id.say(&ctx.http, &format!("Python bot says: {}", content)).await {
                            println!("Error sending message: {:?}", why);
                        }
                    } else {
                        if let Err(why) = msg.channel_id.say(&ctx.http, "No recent messages from Python bot.").await {
                            println!("Error sending message: {:?}", why);
                        }
                    }
                }
                Err(_) => {
                    if let Err(why) = msg.channel_id.say(&ctx.http, "No shared file found.").await {
                        println!("Error sending message: {:?}", why);
                    }
                }
            }
        }
    }

    async fn ready(&self, _: Context, ready: Ready) {
        println!("Rust bot {} is connected!", ready.user.name);
    }
}

#[tokio::main]
async fn main() {
    dotenv().ok();

    let token = env::var("BOT_TOKEN_RS")
        .expect("Expected BOT_TOKEN_RS in environment");

    let intents = GatewayIntents::GUILD_MESSAGES
        | GatewayIntents::DIRECT_MESSAGES
        | GatewayIntents::MESSAGE_CONTENT;

    let mut client = Client::builder(&token, intents)
        .event_handler(Handler)
        .await
        .expect("Error creating client");

    if let Err(why) = client.start().await {
        println!("Client error: {:?}", why);
    }
}
