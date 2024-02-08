import sys
from alembic.config import main

import click
import time
import multiprocessing
import uvicorn
from src.api.services.utils.schedule import run_scheduled_jobs

# This is the initial version of database management
# Without managing migrations


@click.group()
def manager_cli():
    pass


@click.command('createdb')
def create_db():
    from src.db import models
    from src.db import get_engine
    max_retries = 10
    retry_count = 0
    while retry_count < max_retries:
        try:
            models.base_provider.Base.metadata.create_all(get_engine())
            return
        except Exception as e:
            print("Could not establish connection to db", e)
            print("retrying ...")
            retry_count += 1
            time.sleep(2 * retry_count)
    exit(1)


@click.command('dropdb')
def drop_db():
    from src.db import models
    from src.db import get_engine
    models.base_provider.Base.metadata.drop_all(get_engine())


@click.command('run')
def run():
    from src.api.main import app, manager
    ## Start rq worker process
    p = multiprocessing.Process(target=manager.start_rq_worker)
    p.start()

    ## Start fast api server
    p2 = multiprocessing.Process(
        target=uvicorn.run,
        args=(app, ),
        kwargs={
            "host": "0.0.0.0",
            "port": 8000,
            # "ssl_keyfile": "/home/azureuser/backend/key.pem",
            # "ssl_certfile": "/home/azureuser/backend/cert.pem",
            # "ssl_keyfile_password": ""

        })
    p2.start()

    ##
    p3 = multiprocessing.Process(target=run_scheduled_jobs)
    p3.start()

    ## Wait
    p.join()
    p2.join()
    p3.join()


# @click.command('alembic')
# @click.argument('alembic_args', nargs=-1)
# def alembic(alembic_args):
#     # Pass the arguments to Alembic main function
#     sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
#     sys.argv[1:] = ["alembic"] + list(alembic_args)
#     sys.exit(main())

manager_cli.add_command(create_db)
manager_cli.add_command(drop_db)
manager_cli.add_command(run)

if __name__ == '__main__':
    if len(sys.argv) > 0:
        if sys.argv[1] == 'alembic':
            # Pass the arguments to Alembic main function
            sys.argv = sys.argv[1:]
            sys.exit(main())
    manager_cli()
