import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    Context
)
import matplotlib.pyplot as plt
from io import BytesIO

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

SELECT_SECTION, GET_SCHEDULE, GET_EXERCISE, GET_EXERCISE_DETAILS = range(4)

body_parts_keyboard = [['Chest', 'Back'], ['Legs', 'Arms'], ['Abs', 'Cardio']]
exercises_keyboard = {
    'Chest': ['Push-ups', 'Bench Press', 'Dumbbell Fly'],
    'Back': ['Pull-ups', 'Deadlifts', 'Rows'],
    'Legs': ['Squats', 'Lunges', 'Leg Press'],
    'Arms': ['Bicep Curls', 'Tricep Dips', 'Shoulder Press'],
    'Abs': ['Crunches', 'Planks', 'Leg Raises'],
    'Cardio': ['Running', 'Jumping Jacks', 'Cycling']
}
exercise_details = {
    'Push-ups': {'sets': 3, 'repetitions': 15, 'rest_interval': '2 minutes'},
    'Bench Press': {'sets': 3, 'repetitions': 12, 'rest_interval': '3 minutes'},
    'Dumbbell Fly': {'sets': 3, 'repetitions': 12, 'rest_interval': '2 minutes'},
    'Pull-ups': {'sets': 3, 'repetitions': 10, 'rest_interval': '3 minutes'},
    'Deadlifts': {'sets': 4, 'repetitions': 8, 'rest_interval': '3 minutes'},
    'Rows': {'sets': 4, 'repetitions': 10, 'rest_interval': '2 minutes'},
    'Squats': {'sets': 4, 'repetitions': 12, 'rest_interval': '2 minutes'},
    'Lunges': {'sets': 3, 'repetitions': 10, 'rest_interval': '2 minutes'},
    'Leg Press': {'sets': 3, 'repetitions': 12, 'rest_interval': '3 minutes'},
    'Bicep Curls': {'sets': 3, 'repetitions': 12, 'rest_interval': '2 minutes'},
    'Tricep Dips': {'sets': 3, 'repetitions': 12, 'rest_interval': '3 minutes'},
    'Shoulder Press': {'sets': 3, 'repetitions': 10, 'rest_interval': '2 minutes'},
    'Crunches': {'sets': 4, 'repetitions': 15, 'rest_interval': '1 minute'},
    'Planks': {'sets': 3, 'repetitions': 'Hold for 1 minute', 'rest_interval': '1 minute'},
    'Leg Raises': {'sets': 3, 'repetitions': 12, 'rest_interval': '2 minutes'},
    'Running': {'sets': 1, 'repetitions': '20 minutes', 'rest_interval': 'N/A'},
    'Jumping Jacks': {'sets': 1, 'repetitions': '3 sets of 30 seconds', 'rest_interval': '30 seconds between sets'},
    'Cycling': {'sets': 1, 'repetitions': '30 minutes', 'rest_interval': 'N/A'},
}

async def start(update: Update, context: Context) -> int:
    reply_markup = ReplyKeyboardMarkup([["Get Schedule"], ["Get Exercise"]], one_time_keyboard=True)
    await update.message.reply_text(
        "Hi! Let's get started. Select an option:",
        reply_markup=reply_markup
    )
    return SELECT_SECTION

async def select_section(update: Update, context: Context) -> int:
    """Stores the selected section and proceeds accordingly."""
    user_choice = update.message.text
    if user_choice == "Get Schedule":
        await update.message.reply_text("Select the duration for the schedule:", reply_markup=ReplyKeyboardMarkup([["1 Week"], ["1 Month"], ["6 Months"]], one_time_keyboard=True))
        return GET_SCHEDULE
    elif user_choice == "Get Exercise":
        reply_markup = ReplyKeyboardMarkup(body_parts_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            "Select a body part you want to exercise:",
            reply_markup=reply_markup
        )
        return GET_EXERCISE

async def get_schedule(update: Update, context: Context) -> int:
    user_choice = update.message.text
    if user_choice == "1 Week":
        await update.message.reply_text("Here's your weekly schedule:")
        await update.message.reply_text("Monday: Chest Exercises\nPush-ups (3 sets x 15 reps, 3 min intervals)")
        await update.message.reply_text("Tuesday: Back Exercises\nPull-ups (3 sets x 10 reps, 2 min intervals)")
        await update.message.reply_text("Wednesday: Leg Exercises\nSquats (3 sets x 12 reps, 2 min intervals)")
        await update.message.reply_text("Thursday: Rest day")
        await update.message.reply_text("Friday: Arm Exercises\nBicep Curls (3 sets x 12 reps, 2 min intervals)")
        await update.message.reply_text("Saturday: Ab Exercises\nCrunches (3 sets x 20 reps, 1 min intervals)")
        await update.message.reply_text("Sunday: Cardio\nRunning (20 minutes)")
    elif user_choice == "1 Month":
        await update.message.reply_text("Here's your monthly schedule:")
        await update.message.reply_text("Week 1 (Monday): Chest Exercises\nPush-ups (3 sets x 15 reps, 3 min intervals)")
        await update.message.reply_text("Week 1 (Wednesday): Leg Exercises\nSquats (3 sets x 12 reps, 2 min intervals)")
        await update.message.reply_text("Week 2 (Monday): Back Exercises\nPull-ups (3 sets x 10 reps, 2 min intervals)")
        await update.message.reply_text("Week 2 (Wednesday): Arm Exercises\nBicep Curls (3 sets x 12 reps, 2 min intervals)")
        await update.message.reply_text("Week 3 (Monday): Cardio\nRunning (20 minutes)")
        await update.message.reply_text("Week 3 (Wednesday): Ab Exercises\nCrunches (3 sets x 20 reps, 1 min intervals)")
        await update.message.reply_text("Week 4: Rest week")
    elif user_choice == "6 Months":
        await update.message.reply_text("Here's your schedule for the next 6 months:")
        await update.message.reply_text("Month 1 (Week 1): Chest Exercises\nPush-ups (3 sets x 15 reps, 3 min intervals)")
        await update.message.reply_text("Month 1 (Week 2): Back Exercises\nPull-ups (3 sets x 10 reps, 2 min intervals)")
        await update.message.reply_text("Month 2 (Week 1): Leg Exercises\nSquats (3 sets x 12 reps, 2 min intervals)")
        await update.message.reply_text("Month 2 (Week 2): Arm Exercises\nBicep Curls (3 sets x 12 reps, 2 min intervals)")
        await update.message.reply_text("Month 3 (Week 1): Cardio\nRunning (20 minutes)")
        await update.message.reply_text("Month 3 (Week 2): Ab Exercises\nCrunches (3 sets x 20 reps, 1 min intervals)")
        await update.message.reply_text("Month 4: Rest month")
    return ConversationHandler.END

async def get_exercise(update: Update, context: Context) -> int:
    user_choice = update.message.text
    if user_choice not in sum(body_parts_keyboard, []):
        await update.message.reply_text("Please select a valid body part.")
        return GET_EXERCISE

    context.user_data['selected_body_part'] = user_choice
    reply_markup = ReplyKeyboardMarkup([[exercise] for exercise in exercises_keyboard[user_choice]], one_time_keyboard=True)
    await update.message.reply_text(
        f"You've selected {user_choice}. Now choose an exercise from the options:",
        reply_markup=reply_markup
    )

    return GET_EXERCISE_DETAILS

async def get_exercise_details(update: Update, context: Context) -> int:
    user_choice = update.message.text
    selected_body_part = context.user_data.get('selected_body_part')
    if not selected_body_part or user_choice not in exercises_keyboard[selected_body_part]:
        await update.message.reply_text("Invalid selection.")
        return ConversationHandler.END

    exercise_info = exercise_details.get(user_choice)
    if not exercise_info:
        await update.message.reply_text("Exercise details not found.")
        return ConversationHandler.END

    response_message = f"Here's how to perform {user_choice}:\n"
    response_message += f"Sets: {exercise_info['sets']}\n"
    response_message += f"Repetitions: {exercise_info['repetitions']}\n"
    response_message += f"Rest Interval: {exercise_info['rest_interval']}\n"

    await update.message.reply_text(response_message)

    return ConversationHandler.END

async def cancel(update: Update, context: Context) -> int:
    await update.message.reply_text("Operation canceled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def training_graph(update: Update, context: Context) -> None:
    dates = ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05']
    workouts_completed = [3, 5, 4, 6, 7]

    plt.figure(figsize=(10, 6))
    plt.bar(dates, workouts_completed, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Workouts Completed')
    plt.title('Weekly Training Progress')
    plt.xticks(rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await update.message.reply_photo(photo=buffer)

    plt.clf()

def main() -> None:
    """Run the bot."""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_SECTION: [MessageHandler(filters.Regex("^(Get Schedule|Get Exercise)$"), select_section)],
            GET_SCHEDULE: [MessageHandler(filters.Regex("^(1 Week|1 Month|6 Months)$"), get_schedule)],
            GET_EXERCISE: [
                MessageHandler(filters.Regex('^(' + '|'.join(sum(body_parts_keyboard, [])) + ')$'), get_exercise)],
            GET_EXERCISE_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_exercise_details)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler('traininggraph', training_graph))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
