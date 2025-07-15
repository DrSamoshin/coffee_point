# Alembic
## Base command
`alembic init alembic` - применяеться в новом проекте

`alembic revision --autogenerate -m "initial"` - первый коммит

`alembic revision --autogenerate -m "added age column to user"`

`alembic upgrade head` - применять после каждого коммита
