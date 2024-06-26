import os
import uuid
import shutil
import pandas as pd
import sys
import matplotlib.pyplot as plt
from fastapi import HTTPException

class FileService:
    UPLOAD_DIR = "uploads"
    
    def __init__(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    async def saveFile(self, file):
        try:
            file_id = str(uuid.uuid4())
            file_path = os.path.join(self.UPLOAD_DIR, f"{file_id}.csv")
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return file_id
        except Exception as e:
            print ("error in saveFile")
            print (e)
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

    def getSummary(self, file_id):
        try:
            file_path = os.path.join(self.UPLOAD_DIR, f"{file_id}.csv")
            try:
                df = pd.read_csv(file_path)
                
                return df.describe().to_dict()
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
       
        except Exception as e:
            print ("error in getSummary")
            print (e)
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

    def transformData(self, file_id, transformations):
        file_path = os.path.join(self.UPLOAD_DIR, f"{file_id}.csv")
        try:
            df = pd.read_csv(file_path)
            
            for operation, columns in transformations['transformations'].items():
                
                if operation == 'normalize':
                    for column in columns:
                        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
                if operation == 'fill_missing':
                    for column, value in columns.items():
                        df[column].fillna(value, inplace=True)
            transformed_file_id = f"transformed_{file_id}"
            transformed_file_path = os.path.join(self.UPLOAD_DIR, f"{transformed_file_id}.csv")
            df.to_csv(transformed_file_path, index=False)
            
            return transformed_file_id
        except Exception as e:
            print ("error in transformationData")
            print (e)
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            raise HTTPException(status_code=400, detail=f"Error transforming data: {str(e)}")

    def visualizeData(self, file_id, chart_type, columns):
        file_path = os.path.join(self.UPLOAD_DIR, f"{file_id}.csv")
        try:
            df = pd.read_csv(file_path)
            columns_list = columns.split(",")
            for col in columns_list:
                if col not in df.columns:
                    raise HTTPException(status_code=400, detail=f"Column '{col}' not found in the dataset.")
            
            fig, ax = plt.subplots()
            if chart_type == "histogram":
                for col in columns_list:
                    ax.hist(df[col], bins=10, alpha=0.5, label=col)
                ax.legend()
                ax.set_xlabel("Value")
                ax.set_ylabel("Frequency")
                plt.title("Histogram")
            elif chart_type == "scatter":
                if len(columns_list) != 2:
                    raise HTTPException(status_code=400, detail="Scatter plot requires exactly 2 columns.")
                ax.scatter(df[columns_list[0]], df[columns_list[1]])
                ax.set_xlabel(columns_list[0])
                ax.set_ylabel(columns_list[1])
                plt.title("Scatter Plot")
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported chart type '{chart_type}'. Supported types are: histogram, scatter")
            
            plot_filename = f"{file_id}_{uuid.uuid4()}.png"
            plot_path = os.path.join(self.UPLOAD_DIR, plot_filename)
            plt.savefig(plot_path)
            plt.close()
            return plot_path
        except Exception as e:
            print ("error in visualizeData")
            print (e)
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            raise HTTPException(status_code=400, detail=str(e))
