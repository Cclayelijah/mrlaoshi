import discord
from openai import AsyncOpenAI
import random
from datetime import datetime, timedelta
import pytz
import asyncio
import schedule
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
# DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

# Initialize the OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Initialize the Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Ensure the bot can access guild members

discord_client = discord.Client(intents=intents)

GUILD_ID = 1237488266073211001  # Replace with your actual guild ID
JOURNAL_CHANNEL_NAME = "日杂-journals"  # Channel where threads will be created

# Dictionary to store thread IDs for each user
user_threads = {}

# Lists of questions
english_questions = [
    "Suggested daily journal question: Describe your favorite part of the day. (100 words)",
    "Suggested daily journal question: What new thing did you learn today? (100 words)",
    "Suggested daily journal question: What challenge did you overcome today? (100 words)",
    "Suggested daily journal question: Describe a moment when you felt proud. (100 words)",
    "Suggested daily journal question: What is something you're grateful for today? (100 words)",
    "Suggested daily journal question: What made you laugh today? (100 words)",
    "Suggested daily journal question: How did you show kindness today? (100 words)",
    "Suggested daily journal question: Describe a goal you achieved today. (100 words)",
    "Suggested daily journal question: What was the best part of your day? (100 words)",
    "Suggested daily journal question: What did you do for self-care today? (100 words)",
    "Suggested daily journal question: Describe a new experience you had today. (100 words)",
    "Suggested daily journal question: How did you stay positive today? (100 words)",
    "Suggested daily journal question: What is something you look forward to tomorrow? (100 words)",
    "Suggested daily journal question: Describe a moment of peace you experienced today. (100 words)",
    "Suggested daily journal question: What was your favorite meal today and why? (100 words)",
    "Suggested daily journal question: How did you handle stress today? (100 words)",
    "Suggested daily journal question: What is one thing you could improve on tomorrow? (100 words)",
    "Suggested daily journal question: What was the most interesting conversation you had today? (100 words)",
    "Suggested daily journal question: How did you inspire someone today? (100 words)",
    "Suggested daily journal question: What is something you learned about yourself today? (100 words)",
    "Suggested daily journal question: How did you stay focused on your tasks today? (100 words)",
    "Suggested daily journal question: What book or article did you read today? (100 words)",
    "Suggested daily journal question: Describe a beautiful moment you saw today. (100 words)",
    "Suggested daily journal question: What act of kindness did you witness today? (100 words)",
    "Suggested daily journal question: How did you practice patience today? (100 words)",
    "Suggested daily journal question: What is something you appreciate about yourself today? (100 words)",
    "Suggested daily journal question: Describe a creative activity you did today. (100 words)",
    "Suggested daily journal question: What positive habit did you practice today? (100 words)"
]

chinese_questions = [
    "建议每日日志问题: 描述今天你最喜欢的部分。 (100个字)", "建议每日日志问题: 你今天学到了什么新东西？ (100个字)",
    "建议每日日志问题: 你今天克服了什么挑战？ (100个字)", "建议每日日志问题: 描述一个让你感到自豪的时刻。 (100个字)",
    "建议每日日志问题: 今天你感恩的是什么？ (100个字)", "建议每日日志问题: 今天什么让你发笑了？ (100个字)",
    "建议每日日志问题: 今天你是怎么表现出善意的？ (100个字)", "建议每日日志问题: 描述你今天实现的一个目标。 (100个字)",
    "建议每日日志问题: 今天最好的部分是什么？ (100个字)", "建议每日日志问题: 你今天做了什么自我护理？ (100个字)",
    "建议每日日志问题: 描述你今天的新体验。 (100个字)", "建议每日日志问题: 你今天是怎么保持积极的？ (100个字)",
    "建议每日日志问题: 明天你期待什么？ (100个字)", "建议每日日志问题: 描述你今天经历的一个平静时刻。 (100个字)",
    "建议每日日志问题: 今天你最喜欢的一餐是什么，为什么？ (100个字)", "建议每日日志问题: 你今天是怎么应对压力的？ (100个字)",
    "建议每日日志问题: 明天你可以改进什么？ (100个字)", "建议每日日志问题: 今天你进行的最有趣的对话是什么？ (100个字)",
    "建议每日日志问题: 今天你是怎么激励别人的？ (100个字)", "建议每日日志问题: 你今天学到了什么关于自己的事？ (100个字)",
    "建议每日日志问题: 你今天是怎么保持专注的？ (100个字)", "建议每日日志问题: 你今天读了什么书或文章？ (100个字)",
    "建议每日日志问题: 描述你今天看到的一个美丽时刻。 (100个字)", "建议每日日志问题: 今天你目睹了什么善举？ (100个字)",
    "建议每日日志问题: 你今天是怎么练习耐心的？ (100个字)", "建议每日日志问题: 今天你欣赏自己什么？ (100个字)",
    "建议每日日志问题: 描述你今天做的一个创意活动。 (100个字)", "建议每日日志问题: 今天你练习了什么积极习惯？ (100个字)"
]


@discord_client.event
async def on_ready():
    print(f'We have logged in as {discord_client.user}')
    asyncio.create_task(schedule_tasks())


async def schedule_tasks():
    print("Scheduling tasks...")
    # Schedule the tasks at a specific time zone (US/Eastern and Asia/Shanghai)
    tz_eastern = pytz.timezone('US/Eastern')
    tz_china = pytz.timezone('Asia/Shanghai')
    now_eastern = datetime.now(tz_eastern)
    now_china = datetime.now(tz_china)

    target_time_chinese_learners = now_eastern.replace(hour=7,
                                                       minute=0,
                                                       second=0,
                                                       microsecond=0)
    if now_eastern >= target_time_chinese_learners:
        target_time_chinese_learners += timedelta(days=1)

    target_time_english_learners = now_china.replace(hour=7,
                                                     minute=0,
                                                     second=0,
                                                     microsecond=0)
    if now_china >= target_time_english_learners:
        target_time_english_learners += timedelta(days=1)

    delay_chinese_learners = (target_time_chinese_learners -
                              now_eastern).total_seconds()
    delay_english_learners = (target_time_english_learners -
                              now_china).total_seconds()

    print(
        f"Tasks scheduled to run in {delay_chinese_learners} seconds for Chinese learners"
    )
    print(
        f"Tasks scheduled to run in {delay_english_learners} seconds for English learners"
    )

    schedule.every().day.at("07:00").do(asyncio.create_task,
                                        ask_chinese_questions())
    schedule.every().day.at("07:00").do(asyncio.create_task,
                                        ask_english_questions())

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def get_random_question(questions):
    return random.choice(questions)


async def ask_english_questions():
    print("Asking English questions...")
    guild = discord_client.get_guild(GUILD_ID)
    if guild:
        print(f"Found guild: {guild.name}")
        chinese_role = discord.utils.get(guild.roles, name="学习中文")
        if chinese_role:
            print("Found role: 学习中文")
            question = get_random_question(english_questions)
            for member in guild.members:
                if chinese_role in member.roles:
                    try:
                        await member.send(
                            "Hello, your daily journal is ready. Please check your thread under the channel '日杂-journals'."
                        )
                        print(f"Sent question to {member.name}")
                        await send_to_thread(guild, member, question,
                                             "English")
                    except Exception as e:
                        print(f"Failed to send message to {member.name}: {e}")
        else:
            print("Role '学习中文' not found.")
    else:
        print(f"Guild with ID {GUILD_ID} not found.")


async def ask_chinese_questions():
    print("Asking Chinese questions...")
    guild = discord_client.get_guild(GUILD_ID)
    if guild:
        print(f"Found guild: {guild.name}")
        english_role = discord.utils.get(guild.roles, name="Learning English")
        if english_role:
            print("Found role: Learning English")
            question = get_random_question(chinese_questions)
            for member in guild.members:
                if english_role in member.roles:
                    try:
                        await member.send(
                            "你好，你的每日日志已准备好。请检查频道 '日杂-journals' 下的线程。")
                        print(f"Sent question to {member.name}")
                        await send_to_thread(guild, member, question,
                                             "Chinese")
                    except Exception as e:
                        print(f"Failed to send message to {member.name}: {e}")
        else:
            print("Role 'Learning English' not found.")
    else:
        print(f"Guild with ID {GUILD_ID} not found.")


async def send_to_thread(guild, member, question, language="English"):
    journal_channel = discord.utils.get(guild.channels,
                                        name=JOURNAL_CHANNEL_NAME)
    if journal_channel:
        thread_id = user_threads.get(member.id)
        if thread_id:
            thread = await discord_client.fetch_channel(thread_id)
            if thread:
                await thread.send(
                    f"Here is your daily journal prompt:\n\n{question}")
                print(f"Sent question to existing thread for {member.name}")
            else:
                print(f"Thread {thread_id} not found, creating a new one.")
                await create_private_thread(guild, member, question, language)
        else:
            await create_private_thread(guild, member, question, language)
    else:
        print(f"Channel '{JOURNAL_CHANNEL_NAME}' not found.")


async def create_private_thread(guild, member, question, language="English"):
    journal_channel = discord.utils.get(guild.channels,
                                        name=JOURNAL_CHANNEL_NAME)
    if journal_channel:
        try:
            thread_name = f"{member.name}'s {language} Journal"
            thread = await journal_channel.create_thread(
                name=thread_name, type=discord.ChannelType.private_thread)
            await thread.send(
                f"Hello {member.mention}, here is your daily journal prompt:\n\n{question}"
            )
            await thread.add_user(member)
            user_threads[member.id] = thread.id
            print(f"Created private thread for {member.name}")
        except Exception as e:
            print(f"Failed to create thread for {member.name}: {e}")
    else:
        print(f"Channel '{JOURNAL_CHANNEL_NAME}' not found.")


@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    print(f'Received message from {message.author}: {message.content}')

    if "Could you explain" in message.content or "请解释" in message.content:
        response = await handle_follow_up_question(message.content)
        await message.channel.send(response)
    elif message.content.startswith("journal"):
        # Process English journal entry
        journal_content = message.content[len("journal"):].strip()
        word_count = len(journal_content.split())
        print(f"English journal entry word count: {word_count}")
        if word_count < 100:
            await message.channel.send(
                f'Please write at least 100 words. You wrote {word_count} words.'
            )
        else:
            response = await process_message(journal_content, "English")
            await message.channel.send(
                f'Here is the corrected version of your journal entry:\n\n{response}'
            )
            await message.channel.send(
                "If you have any questions about the corrections, please start your follow-up question with 'Could you explain'."
            )
    elif message.content.startswith("日志"):
        # Process Chinese journal entry
        journal_content = message.content[len("日志"):].strip()
        char_count = len(journal_content)
        print(f"Chinese journal entry character count: {char_count}")
        if char_count < 100:
            await message.channel.send(f'请写至少100个字。你写了 {char_count} 个字。')
        else:
            response = await process_message(journal_content, "Chinese")
            await message.channel.send(f'这是你日记的改正版本：\n\n{response}')
            await message.channel.send("如果你对改正有任何问题，请以 '请解释' 开头提问。")


async def process_message(content, language):
    prompt = f"Correct the grammar of the following {language} text:\n\n{content}"
    print(f"Sending prompt to OpenAI: {prompt}")
    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }])
        response = completion.choices[0].message.content.strip()
        print(f"Received response from OpenAI: {response}")
        return response
    except Exception as e:
        print(f"Error in OpenAI call: {e}")
        return f"An error occurred while generating the response: {str(e)}"


async def handle_follow_up_question(question):
    prompt = f"Answer the following question in a clear and helpful manner:\n\n{question}"
    print(f"Sending follow-up question to OpenAI: {prompt}")
    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }])
        response = completion.choices[0].message.content.strip()
        print(f"Received follow-up response from OpenAI: {response}")
        return response
    except Exception as e:
        print(f"Error in follow-up response: {e}")
        return f"An error occurred while generating the response: {str(e)}"


print("Starting the bot...")
discord_client.run(os.environ['DISCORD_BOT_TOKEN'])
print("Bot has started")
