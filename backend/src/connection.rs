use diesel::pg::PgConnection;
use diesel::r2d2::{self, ConnectionManager, PooledConnection};
use rocket::{Request, State};
use rocket::http::Status;
use rocket::request::FromRequest;
use rocket::request::Outcome;
use std::env;
use std::ops::Deref;
use r2d2::Pool;

type DbPool = r2d2::Pool<ConnectionManager<PgConnection>>;

pub fn init_pool() -> DbPool {
    let manager = ConnectionManager::<PgConnection>::new(database_url());
    Pool::builder()
        .max_size(15)
        .build(manager)
        .expect("Failed to create DB Pool")
}

fn database_url() -> String {
    env::var("DATABASE_URL").expect("DATABASE_URL must be set")
}

pub struct DbConn(pub PooledConnection<ConnectionManager<PgConnection>>);

#[rocket::async_trait]
impl<'r> FromRequest<'r> for DbConn {
    type Error = ();

    async fn from_request(request: &'r Request<'_>) -> Outcome<Self, Self::Error> {
        // Use a guard to retrieve the pool from the request state
        let pool = request.guard::<State<DbPool>>().await;
        
        // Check if the pool was successfully retrieved
        match pool {
            Outcome::Success(pool) => {
                // Attempt to get a connection from the pool
                match pool.get() {
                    Ok(conn) => Outcome::Success(DbConn(conn)), // Wrap the connection in DbConn
                    Err(_) => Outcome::Error((Status::ServiceUnavailable, ())), // Handle errors
                }
            }
            Outcome::Error(_) => Outcome::Error((Status::ServiceUnavailable, ())), // Handle pool retrieval failure
            Outcome::Forward(_) => Outcome::Forward(()), // Forward if not a failure or success
        }

        // Attempt to get a connection from the pool
        match pool.get() {
            Ok(conn) => Outcome::Success(DbConn(conn)), // Wrap the connection in DbConn
            Err(_) => Outcome::Error((Status::ServiceUnavailable, ())), // Handle errors
        }
    }
}

impl Deref for DbConn {
    type Target = PgConnection;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}