extern crate actix_rt;
extern crate actix_web;
extern crate database;
extern crate diesel;
extern crate dotenv;
extern crate env_logger;
extern crate juniper;
extern crate r2d2;

use actix_cors::Cors;
use actix_web::{middleware::Logger, web::Data, App, HttpServer};
use database::{db::get_pool, endpoints::register};

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    // Instantiate a new connection pool
    let pool = get_pool();

    HttpServer::new(move || {
        App::new()
            .app_data(Data::new(pool.clone()))
            .configure(register)
            .wrap(Cors::permissive())
            .wrap(Logger::default())
    })
    .bind(("0.0.0.0", 4000))?
    .run()
    .await
}
