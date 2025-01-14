from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

class DBHelper:
	def __init__(self, echo=settings.db_echo):
		self.engine = create_async_engine(
			url=settings.db_url,
			echo=echo,
			)


helper = DBHelper()