from __future__ import annotations
from fastapi import Depends
from core.dependencies.dataset import get_dataset_service
from backend.services.dataset_service import DatasetService
from services.dataset.export_service import ExportService

def get_export_service(dataset_service: DatasetService = Depends(get_dataset_service)) -> ExportService:

    return ExportService(dataset_service=dataset_service)