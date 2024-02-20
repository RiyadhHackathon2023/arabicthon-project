
docker cp ./backend/configs/pg_hba.conf backend_db:/var/lib/postgresql/data/pg_hba.conf
docker restart backend_db