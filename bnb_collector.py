# coding: utf-8
import asyncio
import json
import re
import sys
import os
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn

console = Console()

# Vérification de config.json
if not os.path.isfile("config.json"):
    console.print("[bold red]Erreur : config.json introuvable.[/bold red]")
    sys.exit(1)

# Chargement de la configuration
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except json.JSONDecodeError:
    console.print("[bold red]Erreur : config.json mal formé.[/bold red]")
    sys.exit(1)

# Informations de configuration
api_id = config.get("api_id")
api_hash = config.get("api_hash")
phone = config.get("phone")
bot_username = "@Free_Binance_Bnb_Pay_Bot"

if not all([api_id, api_hash, phone]):
    console.print("[bold red]Erreur : api_id, api_hash ou phone manquant dans config.json.[/bold red]")
    sys.exit(1)

client = TelegramClient("bnb_session", api_id, api_hash)
last_message = ""

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    global last_message
    msg = event.message.message.strip()

    if msg == last_message:
        return
    last_message = msg

    console.print(f"[bold green]Message du bot :[/bold green] {msg}")

    # Clic automatique sur les boutons utiles
    if event.buttons:
        for row in event.buttons:
            for button in row:
                if hasattr(button, "text"):
                    b_text = button.text.lower()
                    if any(keyword in b_text for keyword in ["🎁", "collect", "treasury"]):
                        console.print(f"[bold blue]→ Clic automatique :[/bold blue] {button.text}")
                        try:
                            await button.click()
                            await asyncio.sleep(2)
                        except Exception as e:
                            console.print(f"[bold red]Erreur lors du clic :[/bold red] {e}")

    # Temps d’attente détecté dans le message ou défaut
    match = re.search(r"Wait (\d+) seconds", msg)
    wait_time = int(match.group(1)) if match else 60

    try:
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Attente avant relance...", total=wait_time)
            for _ in range(wait_time):
                await asyncio.sleep(1)
                progress.update(task, advance=1)
    except Exception as e:
        console.print(f"[bold red]Erreur durant l'attente :[/bold red] {e}")

    try:
        await client.send_message(bot_username, "✅ Free Bnb Collect 🎰")
        console.print("[bold green]Commande renvoyée.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Erreur d'envoi :[/bold red] {e}")

async def main():
    try:
        await client.start(phone=phone)
        me = await client.get_me()
        console.print(f"[bold yellow]Connecté avec succès :[/bold yellow] {me.first_name}")

        # Vérification de l'existence du bot
        try:
            await client.get_entity(bot_username)
        except Exception:
            console.print(f"[bold red]Erreur : Le bot {bot_username} est introuvable.[/bold red]")
            return

        await client.send_message(bot_username, "✅ Free Bnb Collect 🎰")
        await client.run_until_disconnected()

    except SessionPasswordNeededError:
        console.print("[bold red]Erreur : Ce compte nécessite une authentification à deux facteurs (2FA).[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Erreur générale :[/bold red] {e}")

with client:
    client.loop.run_until_complete(main())
