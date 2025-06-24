"""
API эндпоинты для управления промтами
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.core.prompts import PromptManager, PromptTemplate, PromptType, get_prompt_manager

router = APIRouter()


class PromptCreateRequest(BaseModel):
    """Запрос на создание промта"""
    name: str
    description: str
    prompt_type: str
    template: str
    parameters: List[str] = []
    version: str = "1.0"
    metadata: Dict[str, Any] = {}


class PromptUpdateRequest(BaseModel):
    """Запрос на обновление промта"""
    name: Optional[str] = None
    description: Optional[str] = None
    template: Optional[str] = None
    parameters: Optional[List[str]] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class PromptResponse(BaseModel):
    """Ответ с информацией о промте"""
    id: str
    name: str
    description: str
    prompt_type: str
    template: str
    parameters: List[str]
    version: str
    is_active: bool
    metadata: Dict[str, Any]


@router.get("/", response_model=Dict[str, Dict[str, Any]])
async def list_prompts(
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Получить список всех промтов
    """
    try:
        return prompt_manager.list_prompts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка промтов: {str(e)}")


@router.get("/types", response_model=List[str])
async def get_prompt_types():
    """
    Получить список доступных типов промтов
    """
    return [pt.value for pt in PromptType]


@router.get("/type/{prompt_type}", response_model=List[PromptResponse])
async def get_prompts_by_type(
    prompt_type: str,
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Получить промты определенного типа
    """
    try:
        pt_enum = PromptType(prompt_type)
        prompts = prompt_manager.get_prompts_by_type(pt_enum)
        
        return [
            PromptResponse(
                id=prompt_id,
                name=prompt.name,
                description=prompt.description,
                prompt_type=prompt.prompt_type.value,
                template=prompt.template,
                parameters=prompt.parameters,
                version=prompt.version,
                is_active=prompt.is_active,
                metadata=prompt.metadata
            )
            for prompt_id, prompt in prompt_manager.prompts.items()
            if prompt.prompt_type == pt_enum and prompt.is_active
        ]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Неизвестный тип промта: {prompt_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения промтов: {str(e)}")


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: str,
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Получить промт по ID
    """
    try:
        prompt = prompt_manager.get_prompt(prompt_id)
        if not prompt:
            raise HTTPException(status_code=404, detail=f"Промт {prompt_id} не найден")
        
        return PromptResponse(
            id=prompt_id,
            name=prompt.name,
            description=prompt.description,
            prompt_type=prompt.prompt_type.value,
            template=prompt.template,
            parameters=prompt.parameters,
            version=prompt.version,
            is_active=prompt.is_active,
            metadata=prompt.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения промта: {str(e)}")


@router.post("/", response_model=PromptResponse)
async def create_prompt(
    request: PromptCreateRequest,
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Создать новый промт
    """
    try:
        # Генерируем ID для нового промта
        prompt_id = f"custom_{request.name.lower().replace(' ', '_')}_{request.version}"
        
        # Проверяем, что промт с таким ID не существует
        if prompt_manager.get_prompt(prompt_id):
            raise HTTPException(status_code=400, detail=f"Промт с ID {prompt_id} уже существует")
        
        # Создаем промт
        prompt = PromptTemplate(
            name=request.name,
            description=request.description,
            prompt_type=PromptType(request.prompt_type),
            template=request.template,
            parameters=request.parameters,
            version=request.version,
            metadata=request.metadata
        )
        
        prompt_manager.add_prompt(prompt_id, prompt)
        
        return PromptResponse(
            id=prompt_id,
            name=prompt.name,
            description=prompt.description,
            prompt_type=prompt.prompt_type.value,
            template=prompt.template,
            parameters=prompt.parameters,
            version=prompt.version,
            is_active=prompt.is_active,
            metadata=prompt.metadata
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка валидации: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания промта: {str(e)}")


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: str,
    request: PromptUpdateRequest,
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Обновить существующий промт
    """
    try:
        # Проверяем, что промт существует
        prompt = prompt_manager.get_prompt(prompt_id)
        if not prompt:
            raise HTTPException(status_code=404, detail=f"Промт {prompt_id} не найден")
        
        # Подготавливаем данные для обновления
        update_data = {}
        if request.name is not None:
            update_data['name'] = request.name
        if request.description is not None:
            update_data['description'] = request.description
        if request.template is not None:
            update_data['template'] = request.template
        if request.parameters is not None:
            update_data['parameters'] = request.parameters
        if request.version is not None:
            update_data['version'] = request.version
        if request.is_active is not None:
            update_data['is_active'] = request.is_active
        if request.metadata is not None:
            update_data['metadata'] = request.metadata
        
        prompt_manager.update_prompt(prompt_id, **update_data)
        
        # Получаем обновленный промт
        updated_prompt = prompt_manager.get_prompt(prompt_id)
        
        return PromptResponse(
            id=prompt_id,
            name=updated_prompt.name,
            description=updated_prompt.description,
            prompt_type=updated_prompt.prompt_type.value,
            template=updated_prompt.template,
            parameters=updated_prompt.parameters,
            version=updated_prompt.version,
            is_active=updated_prompt.is_active,
            metadata=updated_prompt.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления промта: {str(e)}")


@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: str,
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Удалить промт
    """
    try:
        prompt_manager.delete_prompt(prompt_id)
        return {"message": f"Промт {prompt_id} успешно удален"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления промта: {str(e)}")


@router.post("/{prompt_id}/format")
async def format_prompt(
    prompt_id: str,
    parameters: Dict[str, Any],
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Форматировать промт с переданными параметрами
    """
    try:
        formatted_prompt = prompt_manager.format_prompt(prompt_id, **parameters)
        return {"formatted_prompt": formatted_prompt}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка форматирования промта: {str(e)}")


@router.post("/{prompt_id}/activate")
async def activate_prompt(
    prompt_id: str,
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Активировать промт
    """
    try:
        prompt_manager.update_prompt(prompt_id, is_active=True)
        return {"message": f"Промт {prompt_id} активирован"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка активации промта: {str(e)}")


@router.post("/{prompt_id}/deactivate")
async def deactivate_prompt(
    prompt_id: str,
    prompt_manager: PromptManager = Depends(get_prompt_manager)
):
    """
    Деактивировать промт
    """
    try:
        prompt_manager.update_prompt(prompt_id, is_active=False)
        return {"message": f"Промт {prompt_id} деактивирован"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка деактивации промта: {str(e)}") 