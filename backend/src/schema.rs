// @generated automatically by Diesel CLI.

diesel::table! {
    fights (id) {
        id -> Int4,
        fighter_1 -> Text,
        fighter_2 -> Text,
        result -> Text,
        method -> Text,
    }
}
