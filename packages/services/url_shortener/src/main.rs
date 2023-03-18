use warp::{reply::json, Filter, Rejection, Reply, redirect, http::Uri};


pub async fn redirect_to_site(path: String) -> Result<impl Reply, Rejection> {

    let location = Uri::from_static("https://facebook.com");
    println!("{:?}", path);

    Ok(redirect(location))
}

#[tokio::main]
async fn main() {

    let redirection = warp::path!("short" / String)
        .and(warp::get())
        .and_then(redirect_to_site);


    println!("🚀 Server started successfully");
    warp::serve(redirection).run(([0, 0, 0, 0], 8000)).await;
}