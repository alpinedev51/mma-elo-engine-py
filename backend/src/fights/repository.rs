#![allow(proc_macro_derive_resolution_fallback)]
use diesel;
use diesel::prelude::*;
use crate::schema::fights;
use crate::fights::Fight;

pub fn all(connection: &mut PgConnection) -> QueryResult<Vec<Fight>> {
    fights::table.load::<Fight>(connection)
}

pub fn get(id: i32, connection: &mut PgConnection) -> QueryResult<Fight> {
    fights::table.find(id).get_result::<Fight>(connection)
}

pub fn insert(fight: Fight, connection: &mut PgConnection) -> QueryResult<Fight> {
    diesel::insert_into(fights::table)
        .values(&NewFight::from_fight(fight))
        .get_result(connection)
}

pub fn update(id: i32, fight: Fight, connection: &mut PgConnection) -> QueryResult<Fight> {
    diesel::update(fights::table.find(id))
        .set(&fight)
        .get_result(connection)
}

pub fn delete(id: i32, connection: &mut PgConnection) -> QueryResult<usize> {
    diesel::delete(fights::table.find(id))
        .execute(connection)
}

#[derive(Insertable)]
#[diesel(table_name = fights)]
pub struct NewFight {
    pub fighter_1: String,
    pub fighter_2: String,
    pub result: String,
    pub method: String
}

impl NewFight {
    
    fn from_fight(fight: Fight) -> NewFight {
        NewFight {
            fighter_1: fight.fighter_1,
            fighter_2: fight.fighter_2,
            result: fight.result,
            method: fight.method
        }
    }
}