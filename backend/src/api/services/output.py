
from ...db.models import WorkerModel
from ...db.session import get_session
from typing import List
from .responses.service_response import ServiceResponse
from src.neo4j_db.neo4j_connection import get_neo4j_connection

async def update_output_word(self, worker_id, relation_id: str, word):
        session = get_session()
        worker_db: List[WorkerModel] = session.query(WorkerModel).order_by(WorkerModel.start_date.desc())\
            .filter(WorkerModel.worker_id == worker_id)\
            .first()
        if worker_db:
            ## Fetch neo4j connection
            conn = get_neo4j_connection()
            edited = conn.edit_word_by_worker(
                    worker_id=worker_db.worker_id,
                    has_output_id=relation_id,
                    new_word=word,
                )
         
            if edited:
                return ServiceResponse(response_status='success',
                                    data="word edited",
                                    http_code=200,
                                    message='')
            
            else:
                return ServiceResponse(response_status='error',
                                data=None,
                                http_code=500,
                                message='Error editing output word')
                
async def update_output_definition(self, worker_id, relation_id: str, definition):
        session = get_session()
        worker_db: List[WorkerModel] = session.query(WorkerModel).order_by(WorkerModel.start_date.desc())\
            .filter(WorkerModel.worker_id == worker_id)\
            .first()
        
        if worker_db:
            ## Fetch neo4j connection
            conn = get_neo4j_connection()
            edited = conn.edit_definition_by_worker(
                    worker_id=worker_db.worker_id,
                    has_output_id=relation_id,
                    new_definition=definition,
                )
         
            if edited:
                return ServiceResponse(response_status='success',
                                    data="definition edited",
                                    http_code=200,
                                    message='')
            
            else:
                return ServiceResponse(response_status='error',
                                data=None,
                                http_code=500,
                                message='Error editing output definition')