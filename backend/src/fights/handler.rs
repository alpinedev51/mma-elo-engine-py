use crate::connection::DbConn;
use diesel::result::Error;
use std::env;
use crate::fights;
use fights::Fight;
use rocket::http::Status;
use rocket::response::status;
use rocket::serde::json::Json;

#[get("/")]
pub fn all(connection: &mut DbConn) -> Result<Json<Vec<Fight>>, Status> {
    fights::repository::all(connection)
        .map(|fights| Json(fights))
        .map_err(|error| error_status(error))
}

fn error_status(error: Error) -> Status {
    match error {
        Error::NotFound => Status::NotFound,
        _ => Status::InternalServerError
    }
}

#[get("/<id>")]
pub fn get(id: i32, connection: &mut DbConn) -> Result<Json<Fight>, Status> {
    fights::repository::get(id, connection)
        .map(|fight| Json(fight))
        .map_err(|error| error_status(error))
}

#[post("/", format = "application/json", data = "<fight>")]
pub fn post(fight: Json<Fight>, connection: &mut DbConn) -> Result<status::Created<Json<Fight>>, Status> {
    fights::repository::insert(fight.into_inner(), connection)
        .map(|fight| fight_created(fight))
        .map_err(|error| error_status(error))
}

fn fight_created(fight: Fight) -> status::Created<Json<Fight>> {
    status::Created(
        format!("{host}:{port}/fights/{id}", host = host(), port = port(), id = fight.id).to_string(),
        Some(Json(fight)))
}

fn host() -> String {
    env::var("ROCKET_ADDRESS").expect("ROCKET_ADDRESS must be set")
}

fn port() -> String {
    env::var("ROCKET_PORT").expect("ROCKET_PORT must be set")
}

#[put("/<id>", format = "application/json", data = "<fight>")]
pub fn put(id: i32, fight: Json<Fight>, connection: &mut DbConn) -> Result<Json<Fight>, Status> {
    fights::repository::update(id, fight.into_inner(), connection)
        .map(|fight| Json(fight))
        .map_err(|error| error_status(error))
}

#[delete("/<id>")]
pub fn delete(id: i32, connection: &mut DbConn) -> Result<Status, Status> {
    match fights::repository::get(id, connection) {
        Ok(_) => fights::repository::delete(id, connection)
            .map(|_| Status::NoContent)
            .map_err(|error| error_status(error)),
        Err(error) => Err(error_status(error))
    }
}