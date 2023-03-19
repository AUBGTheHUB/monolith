use mongodb::{bson::doc, Client, Database};
use serde::{Deserialize, Serialize};
use std::env;
use std::error::Error;
use std::str::FromStr;
use warp::{http::StatusCode, http::Uri, redirect, reject, reply::json, Filter, Rejection, Reply};

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

#[derive(Debug)]
struct CustomError(StatusCode);

impl reject::Reject for CustomError {}

pub async fn create_short(data: Data) -> Result<impl Reply, Rejection> {
    println!("{:?}", data);

    unsafe {
        if let Err(e) = COLLECTION.clone().unwrap().insert_one(data, None).await {
            eprintln!("Error inserting document: {}", e);
            reject::custom(CustomError(StatusCode::INTERNAL_SERVER_ERROR));
        }
    }

    Ok("endpoint succesfully setup!")
}

static mut COLLECTION: Option<mongodb::Collection<Data>> = None;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let db = get_database().await.unwrap();

    unsafe { COLLECTION = Some(db.collection("shortened_urls")) }

    let redirection = warp::path!("short" / String)
        .and(warp::get())
        .and_then(redirect_to_site);

    let create_short = warp::path!("short")
        .and(warp::post())
        .and(warp::body::json())
        .and_then(create_short);

    let routes = warp::any().and(redirection.or(create_short));

    println!("🚀 Server started successfully");
    warp::serve(routes).run(([0, 0, 0, 0], 8001)).await;
    Ok(())
}
