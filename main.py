from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Цифровой городовой API",
    description="Сервис для работы с обращениями о проблемах городской инфраструктуры",
    version="1.0"
)


# Описываем структуру обращения
class Report(BaseModel):
    category: str
    description: str
    address: str
    status: str = "Опубликовано"


# Временное хранилище обращений
reports = {
    1: Report(
        category="Дороги",
        description="Большая яма на дороге",
        address="ул. Ленина, 10",
        status="Опубликовано"
    ),
    2: Report(
        category="Мусор",
        description="Переполнена урна",
        address="ул. Советская, 212",
        status="В работе"
    ),
    3: Report(
        category="Освещение",
        description="Не работает уличный фонарь",
        address="ул. Гагарина, 25",
        status="Выполнено"
    )
}


# Главная страница
@app.get("/")
def root():
    return {
        "service": "Цифровой городовой",
        "message": "API работает",
        "reports_count": len(reports)
    }


# Получение всех обращений
# status является QUERY-параметром
# Например: /reports?status=Опубликовано
@app.get("/reports")
def get_reports(status: str | None = None):

    if status is None:
        return reports

    return {
        report_id: report
        for report_id, report in reports.items()
        if report.status.lower() == status.lower()
    }


# Получение конкретного обращения
# report_id является PATH-параметром
# Например: /reports/1
@app.get("/reports/{report_id}")
def get_report(report_id: int):

    if report_id not in reports:
        raise HTTPException(
            status_code=404,
            detail="Обращение не найдено"
        )

    return reports[report_id]


# Создание нового обращения
# report передаётся через BODY
@app.post("/reports")
def create_report(report: Report):

    report_id = max(reports.keys(), default=0) + 1

    reports[report_id] = report

    return {
        "message": "Обращение успешно создано",
        "id": report_id,
        "report": report
    }


# Удаление обращения
@app.delete("/reports/{report_id}")
def delete_report(report_id: int):

    if report_id not in reports:
        raise HTTPException(
            status_code=404,
            detail="Обращение не найдено"
        )

    deleted_report = reports.pop(report_id)

    return {
        "message": "Обращение удалено",
        "report": deleted_report
    }