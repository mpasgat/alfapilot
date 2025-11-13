from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.keyboards import document_types_menu
from bot.states.document_states import DocumentStates

router = Router()


@router.message(F.text == "📑 Документы и письма")
async def documents_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "📄 Документы и письма\n\nВыберите тип документа:",
        reply_markup=document_types_menu,
    )
    await state.set_state(DocumentStates.choosing_type)


@router.message(DocumentStates.choosing_type)
async def process_document_type(message: types.Message, state: FSMContext):
    doc_type = message.text
    await message.answer(
        f"📝 Создание {doc_type}\n\nОпишите, что должно быть в документе:"
    )
    await state.set_state(DocumentStates.waiting_for_content)


@router.message(DocumentStates.waiting_for_content)
async def process_document_content(message: types.Message, state: FSMContext):
    content = message.text
    # TODO: Сгенерировать документ через AI
    await message.answer(
        "✅ Документ создан!\n\n"
        "[Здесь будет сгенерированный документ]\n\n"
        "Предлагаю исправления:\n"
        "[Здесь будут предложения по исправлениям]"
    )
    await state.clear()
