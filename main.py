from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import pandas as pd
import numpy as np
from FileService import FileService


app = FastAPI()
file_service = FileService()


UPLOAD_DIR = "uploads"


app.mount("/C:/RubiScape/DatasetFactory", StaticFiles(directory=UPLOAD_DIR), name="files")

class FileAPI:
    
    @staticmethod
    @app.post("/upload")
    async def uploadFile(file: UploadFile = File(...)):
        file_id = await file_service.saveFile(file)
        return JSONResponse(content={"message": "File uploaded successfully", "file_id": file_id})

    @staticmethod
    @app.get("/summary/{file_id}")
    async def getSummary(file_id: str):
        
        summary = file_service.getSummary(file_id)
        summary = pd.DataFrame(summary)
        summary.fillna("NaN", inplace=True)
        summary.replace({np.inf: "inf", -np.inf: "inf", None: "None"}, inplace=True)
        
        summary = summary.T.to_dict(orient='index')

        return JSONResponse(content=summary)

    @staticmethod
    @app.post("/transform/{file_id}")
    async def transformData(file_id: str, transformations: dict):
        transformed_file_id = file_service.transformData(file_id, transformations)
        return {"message": "Transformations applied successfully", "file_id": transformed_file_id}

    @staticmethod
    @app.get("/visualize/{file_id}")
    async def visualizeData(file_id: str, chart_type: str = Query(..., description="Type of chart: histogram, scatter"), columns: str = Query(..., description="Columns to visualize")):
        plot_path = file_service.visualizeData(file_id, chart_type, columns)
        plot_url = f"http://127.0.0.1:5049/files/{plot_path}"  # Adjust URL as per your server configuration
        plot_path = os.path.join(file_service.UPLOAD_DIR, plot_path)
        res = {
                "message": "Visualization created successfully",
                "plot_url": plot_url,
                "file_path": plot_path  # Return the local file path as well if needed
            }
        return JSONResponse(content=res)
    
    @staticmethod
    @app.get("/files/{file_path:path}", response_class=FileResponse)
    async def serveFile(file_path: str):
        return FileResponse(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049, reload=True)


