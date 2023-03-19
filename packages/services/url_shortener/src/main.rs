use serde::{Deserialize, Serialize};
use warp::{reply::json, Filter, Rejection, Reply, redirect, http::Uri, http::StatusCode, reject};
use mongodb::{Client, Database, Collection, bson::doc};
use mongodb::bson::{Bson, Document};
use std::borrow::Borrow;
use std::env;
use std::error::Error;

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

    let location = Uri::from_static("https://facebook.com");
    println!("{:?}", path);

    Ok(redirect(location))
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Data {
    url: String,
    endpoint: String
}


#[derive(Debug)]
struct CustomError(StatusCode);

impl reject::Reject for CustomError {}

pub async fn create_short(data: Data, collection: Collection<Data>) -> Result<impl Reply, Rejection> {

    println!("{:?}", data);

    if let Err(e) = collection.insert_one(data, None).await {
        eprintln!("Error inserting document: {}", e);
        reject::custom(CustomError(StatusCode::INTERNAL_SERVER_ERROR));
    } 

    Ok("endpoint succesfully setup!")
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {

    let db = get_database().await.unwrap();

    let collection: Collection<Data>= db.collection("shortened_urls");

    let redirection = warp::path!("short" / String)
        .and(warp::get())
        .and_then(redirect_to_site);

    let create_short = warp::path!("short")
    .and(warp::post())
    .and(warp::body::json())
    .and(warp::any().map(move || collection.clone()))
    .and_then(create_short);

    let routes = warp::any().and(redirection.or(create_short));

    println!("🚀 Server started successfully");
    warp::serve(routes).run(([0, 0, 0, 0], 8001)).await;
    Ok(())
}