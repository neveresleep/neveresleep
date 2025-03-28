import os
import json
from pathlib import Path

def handler(request):
    # Получаем базовую директорию
    base_dir = Path(__file__).resolve().parent.parent
    structure = {}
    
    # Проверяем существование основных файлов и директорий
    structure["base_directory_exists"] = os.path.exists(str(base_dir))
    structure["templates_directory_exists"] = os.path.exists(str(base_dir / "templates"))
    structure["static_directory_exists"] = os.path.exists(str(base_dir / "static"))
    structure["index_html_exists"] = os.path.exists(str(base_dir / "templates" / "index.html"))
    
    # Получаем список файлов в основных директориях
    structure["api_files"] = os.listdir(str(base_dir / "api")) if os.path.exists(str(base_dir / "api")) else []
    structure["templates_files"] = os.listdir(str(base_dir / "templates")) if os.path.exists(str(base_dir / "templates")) else []
    structure["static_files"] = os.listdir(str(base_dir / "static")) if os.path.exists(str(base_dir / "static")) else []
    
    # Пытаемся получить содержимое index.html
    try:
        if os.path.exists(str(base_dir / "templates" / "index.html")):
            with open(str(base_dir / "templates" / "index.html"), "r", encoding="utf-8") as f:
                structure["index_html_content_sample"] = f.read(100) + "..." # Первые 100 символов
        else:
            structure["index_html_content_sample"] = "File does not exist"
    except Exception as e:
        structure["index_html_content_sample"] = f"Error reading file: {str(e)}"
    
    # Информация о системе
    structure["current_directory"] = os.getcwd()
    structure["parent_directory"] = str(base_dir)
    structure["environment_variables"] = {k: v for k, v in os.environ.items() if not k.startswith("AWS_")}
    
    # Форматируем результат
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(structure, indent=2)
    } 