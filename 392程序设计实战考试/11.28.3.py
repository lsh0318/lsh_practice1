from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
import io
import uvicorn
from fastapi.responses import StreamingResponse
from typing import Dict


app1 = FastAPI()


def analyze_data1(df: pd.DataFrame):
    avg_salary = df.groupby("district")["salary"].mean().round(2)
    min_salary = df.groupby("district")["salary"].min().round(2)
    max_salary = df.groupby("district")["salary"].max().round(2)

    result_df = pd.DataFrame({
        "avg_salary": avg_salary,
        "min_salary": min_salary,
        "max_salary": max_salary
    })

    result_df = result_df.reset_index()
    result_df.columns = ["district", "平均薪资", "最低薪资", "最高薪资"]

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=True, sheet_name="薪资分析")
    output.seek(0)
    return output



@app1.post("/analyze/salary_by_district")
async def analyze_salary(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File type not supported.")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        if not all(col in df.columns for col in ['district', 'salary']):
            raise HTTPException(status_code=400, detail="文件缺少必要的列")
        excel_stream = analyze_data1(df)
        return StreamingResponse(
            excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=薪资分析.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
app2 = FastAPI()


def analyze_data2(df):
    company_count = df.groupby("district")["company"].count().reset_index(names="公司数量")

    data = pd.DataFrame(company_count)

    region = data['district']
    company_counts = data['公司数量']

    plt.figure(figsize=(10, 6))
    plt.bar(region,company_counts,color='b')

    plt.title('公司数量柱状图',fontsize=16)
    plt.xlabel('地区',fontsize=12)
    plt.ylabel('公司数量',fontsize=12)

    image = io.BytesIO()
    plt.savefig(
        image,
        format='png',
        dpi=300,
        bbox_inches='tight'
    )
    image.seek(0)
    plt.close()
    return image

@app2.post("/analyze/company-distribution/")






