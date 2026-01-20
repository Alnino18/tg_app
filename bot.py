import asyncio
import json
import os
import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, WebAppInfo
from fpdf import FPDF

# --- ДАННЫЕ БОТА ---

TOKEN = '7598063145:AAFBQFceoEI8_9BzXQ2t3pPvb58_wpc4qc8'
GROUP_ID = -1003399244861  # ID вашей группы (с -100)
URL = 'https://alnino18.github.io/tg-app/' # Ссылка на index.html

bot = Bot(token=TOKEN)
dp = Dispatcher()

def create_pdf(order_data, location, user_name):
    pdf = FPDF()
    pdf.add_page()
    
    # Шрифты и Лого
    if os.path.exists("DejaVuSans.ttf"):
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.add_font("DejaVu", "B", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "", 12)
    
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=10, y=10, w=25)

    # Шапка
    pdf.set_font("DejaVu", "B", 18)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(30)
    pdf.cell(160, 15, "НАКЛАДНАЯ", ln=True)
    
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(30)
    pdf.cell(160, 5, f"Цех: {location} | Сотрудник: {user_name}", ln=True)
    pdf.cell(30)
    pdf.cell(160, 5, f"Дата: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True)
    pdf.ln(15)

    # Таблица (Заголовок)
    pdf.set_fill_color(255, 94, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(15, 12, "№", fill=True, align='C')
    pdf.cell(125, 12, " Наименование товара", fill=True)
    pdf.cell(50, 12, "Кол-во", fill=True, align='C')
    pdf.ln()

    # Таблица (Строки)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("DejaVu", "", 11)
    for i, item in enumerate(order_data, 1):
        pdf.cell(15, 10, str(i), border='B', align='C')
        pdf.cell(125, 10, f" {item['name']}", border='B')
        pdf.cell(50, 10, f"{item['qty']} {item['unit']}", border='B', align='C')
        pdf.ln()

    name = f"invoice_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
    pdf.output(name)
    return name

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text="Открыть меню салатов", web_app=WebAppInfo(url=URL))]]
    await message.answer("Бот готов к работе. Нажмите кнопку, чтобы создать накладную.", 
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.web_app_data)
async def web_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        await message.answer("🛠 Создаю накладную...")
        
        path = create_pdf(data['order'], data['location'], message.from_user.full_name)
        await message.answer_document(FSInputFile(path), caption=f"✅ Накладная готова для: {data['location']}")
        
        os.remove(path)
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
