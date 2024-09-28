use crate::fights;
use rocket::*;
use crate::connection;

pub fn create_routes() {
    rocket::build()
        .manage(connection::init_pool())
        .mount("/fights",
            routes![fights::handler::all,
                fights::handler::get,
                fights::handler::post,
                fights::handler::put,
                fights::handler::delete],
            ).launch();
}