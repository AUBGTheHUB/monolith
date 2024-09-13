use mongodb::{bson::doc, Client, Database};
use serde::{Deserialize, Serialize};
use std::env;
use std::error::Error;
use std::str::FromStr;
use warp::{http::Uri, redirect, Filter, Rejection, Reply};

async fn get_database() -> Result<Database, Box<dyn Error>> {
    // Load the MONGO_URI environment variable from the .env file
    dotenv::dotenv().ok();
    let mongo_uri = env::var("MONGOURI")?;

    // Connect to the database and return a Database object
    let client = Client::with_uri_str(&mongo_uri).await?;
    let db = client.database("ShortenedUrlsDB");
    Ok(db)
}

pub async fn redirect_to_site(path: String) -> Result<impl Reply, Rejection> {
    let filter = doc! {"endpoint": &path};

    unsafe {
        if let Ok(document) = COLLECTION.clone().unwrap().find_one(filter, None).await {
            if let Some(document) = document {
                let location = Uri::from_str(&document.url).unwrap();
                return Ok(redirect(location));
            }
        }
    }

    Err(warp::reject::not_found())
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Data {
    url: String,
    endpoint: String,
}

static mut COLLECTION: Option<mongodb::Collection<Data>> = None;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let db = get_database().await.unwrap();

    unsafe { COLLECTION = Some(db.collection("shortened_urls")) }

    let redirection = warp::path!("s" / String)
        .and(warp::get())
        .and_then(redirect_to_site);

    let routes = warp::any().and(redirection);

    println!("🚀 Server started successfully");
    warp::serve(routes).run(([0, 0, 0, 0], 8001)).await;
    Ok(())
}
