import asyncio
import json
import os
import sys
import re
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()
lock = asyncio.Lock()

console.print(Panel.fit("[bold cyan]<====>> TS BNB AUTOCLICK <<====>[/bold cyan]\n[green]CREE PAR TAHIRY TS[/green]", border_style="bold magenta"))

# Fanamarinana raha misy ilay config.json
if not os.path.isfile("config.json"):
    console.print(Panel.fit("[bold red]Hadisoana: config.json tsy hita.[/bold red]", border_style="red"))
    sys.exit(1)

# Famakiana ilay config
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except json.JSONDecodeError:
    console.print(Panel.fit("[bold red]Hadisoana: tsy mety ilay endriky ny config.json[/bold red]", border_style="red"))
    sys.exit(1)

# Fangalana ny angon-drakitra
api_id = config.get("api_id")
api_hash = config.get("api_hash")
phone = config.get("phone")
bot_username = "Free_Binance_Bnb_Pay_Bot"

client = TelegramClient("bnb_session", api_id, api_hash)
reward_history = set()

async def collect_bnb():
    global reward_history
    while True:
        try:
            console.print("[bold blue]→ Mandefa baiko :[/bold blue] ✅ Free Bnb Collect 🎰")
            await client.send_message(bot_username, "✅ Free Bnb Collect 🎰")
            await asyncio.sleep(1)

            messages = await client.get_messages(bot_username, limit=4)
            wait_time = 60

            for response in messages:
                msg = response.message
                if not msg or not isinstance(msg, str):
                    continue
                msg = msg.strip()

                if "Free Bnb Collect" in msg:
                    continue

                if "successfully collected" in msg.lower() and msg not in reward_history:
                    reward_history.add(msg)
                    console.print(Panel.fit(f"[bold green]Valisoa azonao :[/bold green]\n{msg}", border_style="green"))
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("bnb_log.txt", "a") as log_file:
                        log_file.write(f"[{now}] {msg}\n")
                    continue

                console.print(Panel.fit(f"[bold green]→ Hafatra voaray :[/bold green]\n{msg}", border_style="green"))

                match = re.search(r"again in (\d+) seconds", msg)
                if match:
                    wait_time = int(match.group(1))

                if response.buttons:
                    for row in response.buttons:
                        for button in row:
                            if "collect" in button.text.lower() or "🔮" in button.text.lower():
                                console.print(f"[bold blue]→ Tsindrio :[/bold blue] [yellow]{button.text}[/yellow]")
                                await button.click()
                                break
                else:
                    if not any(x in msg.lower() for x in ["treasury", "reward"]):
                        console.print("[bold red]Tsy nisy bokotra hita tao amin'ny valin'ny bot.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Hadisoana: {e}[/bold red]")

        now = datetime.now().strftime("%H:%M")
        console.print(f"[bold cyan][TS {now}] ⏳ Miandry {wait_time} segondra...[/bold cyan]")

        with Progress(
            SpinnerColumn(),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[bold green]⏳ Miandry...", total=wait_time)
            for _ in range(wait_time):
                await asyncio.sleep(1)
                progress.update(task, advance=1)

async def main():
    try:
        await client.connect()
        if not await client.is_user_authorized():
            console.print(Panel.fit("[bold yellow]Fidirana voalohany : mila manamarina kaody[/bold yellow]", border_style="yellow"))
            await client.send_code_request(phone)
            code = console.input("[bold cyan]→ Ampidiro ny kaody nalefa (Telegram/SMS) : [/bold cyan]")
            try:
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                console.print("[bold red]Mila tenimiafina fanampiny (2FA).[/bold red]")
                password = console.input("[bold yellow]→ Ampidiro ny tenimiafina 2FA : [/bold yellow]")
                await client.sign_in(password=password)

        console.print(Panel.fit("[bold green]✅ Fidirana nahomby![/bold green]\nManomboka ny fitrandrahana BNB...", border_style="green"))
        await collect_bnb()

    except Exception as e:
        console.print(Panel.fit(f"[bold red]Hadisoana fanombohana: {e}[/bold red]", border_style="red"))

with client:
    client.loop.run_until_complete(main())
