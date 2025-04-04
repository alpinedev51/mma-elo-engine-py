from sqlalchemy import text
from .database import engine, Base
from . import models

create_function_sql = """
CREATE OR REPLACE FUNCTION get_elo_records_by_fighter(
    fighter_name_arg TEXT,
    sort_order_arg TEXT
)
RETURNS TABLE (
    fighter_id INTEGER,
    fighter_name TEXT,
    total_fights INTEGER,
    id INTEGER,
    elo_rating DOUBLE PRECISION,
    event_name TEXT,
    event_date DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY EXECUTE format(
        $fmt$
        SELECT
            f.id AS fighter_id,
            f.fighter_name::TEXT,
            COUNT(er.id) OVER (PARTITION BY f.id)::INTEGER AS total_fights,
            er.id,
            er.elo_rating,
            e.event_name::TEXT,
            e.event_date
        FROM fighters f
        JOIN elo_records er ON f.id = er.fighter_id
        JOIN events e ON er.event_id = e.id
        WHERE f.fighter_name ILIKE '%%' || $1 || '%%'
        ORDER BY f.id, e.event_date %s
        $fmt$,
        CASE WHEN lower(sort_order_arg) = 'asc' THEN 'ASC' ELSE 'DESC' END
    )
    USING fighter_name_arg;
END;
$$;
"""

def init_db():
    print("Initializing the database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

    # Execute SQL function
    with engine.begin() as connection:
        try:
            connection.execute(text(create_function_sql))
            print("PostgreSQL function created successfully.")
        except Exception as e:
            print("Function creation failed:", e)

if __name__ == "__main__":
    init_db()
