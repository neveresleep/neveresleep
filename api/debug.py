import json
import sys
import traceback

# Функция-обертка для отлавливания и логирования ошибок
def debug_handler(original_handler):
    def wrapper(request):
        print(f"DEBUG: Получен запрос на путь: {request.path}")
        print(f"DEBUG: Метод запроса: {request.method}")
        print(f"DEBUG: Заголовки запроса: {json.dumps(dict(request.headers))}")
        
        try:
            if request.body:
                print(f"DEBUG: Тело запроса: {request.body.decode('utf-8')}")
        except:
            print("DEBUG: Не удалось декодировать тело запроса")
        
        try:
            response = original_handler(request)
            print(f"DEBUG: Успешный ответ со статусом: {getattr(response, 'status', 'Unknown')}")
            return response
        except Exception as e:
            print(f"DEBUG: ОШИБКА: {str(e)}")
            print("DEBUG: Трассировка стека:")
            traceback.print_exc(file=sys.stdout)
            
            # Возвращаем информативный ответ об ошибке
            error_message = {
                "error": str(e),
                "traceback": traceback.format_exc(),
                "path": request.path,
                "method": request.method
            }
            
            from flask import Response
            return Response(
                json.dumps(error_message),
                status=500,
                content_type="application/json"
            )
    
    return wrapper

# Для активации отладки нужно импортировать основной обработчик 
# и обернуть его этим отладчиком:
#
# from index import handler as original_handler
# handler = debug_handler(original_handler)
#
# Затем закомментировать оригинальный обработчик в index.py 