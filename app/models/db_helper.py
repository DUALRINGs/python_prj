from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session
from config import settings
from asyncio import current_task

class DBHelper:
	def __init__(self, echo=settings.db_echo):
		self.engine = create_async_engine(
			url=settings.db_url,
			echo=echo,
			)
		self.session_factory = async_sessionmaker(
			bind=self.engine,
			autoflush=False,
			autocommit=False,
			expire_on_commit=False,
			)
		
	def get_scoped_session(self):
		session = async_scoped_session(
			session_factory=self.session_factory,
			scopefunc=current_task,
		)
		return session

	async def session_dependency(self) -> AsyncSession:
		async with self.session_factory() as session:
			yield session
			await session.close()

	async def scoped_session_dependency(self) -> AsyncSession:
		session = self.get_scoped_session()
		yield session
		await session.close()


helper = DBHelper()