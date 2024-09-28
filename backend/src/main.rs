#![feature(decl_macro, proc_macro_hygiene)]
#[macro_use] extern crate rocket;
#[macro_use] extern crate diesel;
extern crate dotenvy;
extern crate r2d2;
extern crate r2d2_diesel;
#[macro_use]
extern crate serde_derive;

use dotenvy::dotenv;

mod fights;
mod schema;
mod connection;

fn main() {
    dotenv().ok();
    fights::router::create_routes();
}