use super::schema::fights;

pub mod handler;
pub mod router;
pub mod repository;

#[derive(Queryable, AsChangeset, Serialize, Deserialize)]
#[diesel(table_name = fights)]
#[diesel(check_for_backend(diesel::sqlite::Sqlite))]
pub struct Fight {
    pub id: i32,
    pub fighter_1: String,
    pub fighter_2: String,
    pub result: String,
    pub method: String
}