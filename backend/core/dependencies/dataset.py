from __future__ import annotations
from fastapi import Depends
from core.dependencies.repositories import get_dataset_repository, get_document_repository
from repositories.dataset_repository import DatasetRepository
from repositories.document_repository import DocumentRepository
from services.dataset.dataset_statistics_service import DatasetStatisticsService
from backend.services.dataset_service import DatasetService

def get_dataset_statistics_service(
    dataset_repository: DatasetRepository = Depends(get_dataset_repository),
    document_repository: DocumentRepository = Depends(get_document_repository)
) -> DatasetStatisticsService:

    return DatasetStatisticsService( dataset_repository=dataset_repository, document_repository=document_repository)

def get_dataset_service(
    dataset_repository: DatasetRepository = Depends(get_dataset_repository),
    statistics_service: DatasetStatisticsService = Depends(get_dataset_statistics_service)
) -> DatasetService:

    return DatasetService(dataset_repository=dataset_repository, statistics_service=statistics_service)