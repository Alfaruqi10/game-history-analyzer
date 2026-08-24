"""Data import endpoints"""
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.import_service import ImportService
from app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["import"])


@router.post("/history/import")
async def import_history(
    file: UploadFile = File(...),
    user_id: str = Form(None),
    db: Session = Depends(get_db)
):
    """Impor riwayat dari file CSV atau JSON"""
    try:
        # Read file
        content = await file.read()
        content_str = content.decode("utf-8")
        
        # Determine format
        filename_lower = file.filename.lower()
        
        if filename_lower.endswith(".json"):
            result = ImportService.import_from_json(db, content_str, user_id)
        elif filename_lower.endswith(".csv"):
            result = ImportService.import_from_csv(db, content_str, user_id)
        else:
            raise HTTPException(status_code=400, detail="Format file tidak didukung (gunakan CSV atau JSON)")
        
        logger.info(f"Impor selesai: {result['saved']} tersimpan, {result['skipped']} dilewati")
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error impor file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {str(e)}")
