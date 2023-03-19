use mongodb::{bson::doc, Client, Database};
use serde::{Deserialize, Serialize};
use std::env;
use std::error::Error;
use std::str::FromStr;
use warp::{http::StatusCode, http::Uri, redirect, reject, Filter, Rejection, Reply};

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

#[derive(Debug, Serialize)]
struct ResponseMessage {
    message: String,
}

impl reject::Reject for CustomError {}
impl reject::Reject for ResponseMessage {}

pub async fn create_short(data: Data) -> Result<impl Reply, Rejection> {
    println!("{:?}", data);

    unsafe {
        let collection = COLLECTION.clone().unwrap();
        let filter = doc! {"endpoint": &data.endpoint};
        let result = COLLECTION.clone().unwrap().find_one(filter, None).await;

        if let Ok(Some(_)) = result {
            let json = warp::reply::json(&ResponseMessage {
                message: "Endpoint already exists!".to_owned(),
            });

            return Ok(warp::reply::with_status(json, StatusCode::BAD_REQUEST));
        }

        if let Err(e) = collection.insert_one(data, None).await {
            eprintln!("Error inserting document: {}", e);

            let json = warp::reply::json(&ResponseMessage {
                message: "Couldn't insert new endpoint".to_owned(),
            });

            return Ok(warp::reply::with_status(
                json,
                StatusCode::INTERNAL_SERVER_ERROR,
            ));
        }

        let json = warp::reply::json(&ResponseMessage {
            message: "Document was successfully inserted".to_owned(),
        });
        Ok(warp::reply::with_status(json, StatusCode::ACCEPTED))
    }
}

static mut COLLECTION: Option<mongodb::Collection<Data>> = None;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let db = get_database().await.unwrap();

    unsafe { COLLECTION = Some(db.collection("shortened_urls")) }

    let redirection = warp::path!("s" / String)
        .and(warp::get())
        .and_then(redirect_to_site);

    let create_short = warp::path!("s")
        .and(warp::post())
        .and(warp::body::json())
        .and_then(create_short);

    let routes = warp::any().and(redirection.or(create_short));

    println!("🚀 Server started successfully");
    warp::serve(routes).run(([0, 0, 0, 0], 8001)).await;
    Ok(())
}
