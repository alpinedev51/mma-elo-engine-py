# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from itemadapter import ItemAdapter
from backend.app.models import Fighter, Fight, Event, EloRecord


class MmaScraperPipeline:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_url=crawler.settings.get("DATABASE_URL"),
        )

    def open_spider(self, spider):
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.commit()  # Commit any remaining changes
        self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # handle events
        # If event isn't already in Event table, then add to table
        event_name = adapter.get("event_name_info")
        event_date = adapter.get("event_date_info")
        event = self.session.query(Event).filter_by(event_name=event_name).first()
        if not event:
            event = Event(event_name=event_name, event_date=event_date)
            self.session.add(event)
            self.session.commit()

        # handle fighters
        fighter_1_name = adapter.get("fighter_1_name_info")
        fighter_2_name = adapter.get("fighter_2_name_info")

        fighter_1 = self.session.query(Fighter).filter_by(fighter_name=fighter_1_name).first()
        if not fighter_1:
            fighter_1 = Fighter(fighter_name=fighter_1_name, elo_rating=1000)
            self.session.add(fighter_1)
            self.session.commit()
            
            initial_elo_1 = EloRecord(fighter_id=fighter_1.id, elo_rating=fighter_1.elo_rating, event_id=event.id)
            self.session.add(initial_elo_1)

        fighter_2 = self.session.query(Fighter).filter_by(fighter_name=fighter_2_name).first()
        if not fighter_2:
            fighter_2 = Fighter(fighter_name=fighter_2_name, elo_rating=1000)
            self.session.add(fighter_2)
            self.session.commit()
            
            initial_elo_1 = EloRecord(fighter_id=fighter_2.id, elo_rating=fighter_2.elo_rating, event_id=event.id)
            self.session.add(initial_elo_1)

        # handle fights
        fight = Fight(
            fighter_1_id=fighter_1.id,
            fighter_2_id=fighter_2.id,
            result=adapter.get("result_info"),
            method=adapter.get("method_info"),
            event_id=event.id
        )
        self.session.add(fight)
        self.session.commit()

        return item
