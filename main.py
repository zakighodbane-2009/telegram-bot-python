import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# إعداد قاعدة البيانات
def setup_db():
    conn = sqlite3.connect('countes.db')
    cr = conn.cursor()
    cr.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT, first_name TEXT)')
    conn.commit()
    conn.close()

# حفظ المستخدم
def save_user(user_id, username, first_name):
    conn = sqlite3.connect('countes.db')
    cr = conn.cursor()
    cr.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    exists = cr.fetchone()

    if not exists:
        cr.execute('INSERT INTO users (id, user_name, first_name) VALUES (?, ?, ?)',
                   (user_id, username, first_name))
        conn.commit()

    cr.execute('SELECT COUNT(*) FROM users')
    count = cr.fetchone()[0]

    conn.close()
    return exists is None, count

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_new, count = save_user(user.id, user.username, user.first_name)

    if is_new:
        await update.message.reply_text(
            f"🎉 أهلاً بك يا {user.first_name}!\n"
            f"✅ تم تسجيلك بنجاح.\n"
            f"📊 ترتيبك في قائمة المشتركين هو: {count}."
        )

        if count == 50:
            await update.message.reply_text(
                "🎊 تهانينا! 🎊\n"
                "🎯 لقد كنت المشترك رقم 50!\n"
                "🎁 ترقب مفاجأة أو هدية خاصة قريبًا 😉"
            )
        else:
            await update.message.reply_text(
                "🚀 استمر في دعم البوت وشاركه مع أصدقائك!\n"
                "قد تكون أنت الفائز في التحدي القادم!"
            )
    else:
        await update.message.reply_text(
            f"👋 مرحبًا مجددًا يا {user.first_name}!\n"
            "⚠️ لقد قمت بالتسجيل مسبقًا.\n"
            "🧠 لا يمكن المحاولة أكثر من مرة لضمان العدالة للجميع."
        )

# تشغيل البوت
setup_db()
app = ApplicationBuilder().token('7970480934:AAE6NrkAnuvs9Q75za4kJEgjobnp9Y_g1_Y').build()
app.add_handler(CommandHandler('start', start))
app.run_polling()
