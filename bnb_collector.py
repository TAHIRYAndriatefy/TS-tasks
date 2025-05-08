import asyncio
import json
import re
import sys
import os
from telethon import TelegramClient, events
from rich.console import Console
from rich.progress import Progress

console = Console()

# Vérification du fichier config.json
if not os.path.isfile("config.json"):
    console.print("[bold red]Erreur : le fichier config.json est introuvable.[/bold red]")
    sys.exit(1)

# Chargement de la configuration
with open("config.json", "r") as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError:
        console.print("[bold red]Erreur : config.json est mal formé.[/bold red]")
        sys.exit(1)

api_id = config.get("api_id")
api_hash = config.get("api_hash")
phone = config.get("phone")
bot_username = "Free_Binance_Bnb_Pay_Bot"

client = TelegramClient("bnb_session", api_id, api_hash)

# Pour éviter les répétitions
last_message = ""

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    global last_message
    msg = event.message.message

    # Ignorer les doublons exacts
    if msg == last_message:
        return
    last_message = msg

    console.print(f"[bold green]Réponse du bot :[/bold green] {msg}")

    # Clic automatique si bouton détecté
    if event.buttons:
        for row in event.buttons:
            for button in row:
                if hasattr(button, "text"):
                    b_text = button.text.lower()
                    if "🎁" in b_text or "collect" in b_text or "treasury" in b_text:
                        console.print(f"[bold blue]→ Clic automatique sur :[/bold blue] {button.text}")
                        try:
                            await button.click()
                            await asyncio.sleep(2)
                        except Exception as e:
                            console.print(f"[bold red]Erreur lors du clic :[/bold red] {e}")

    # Temps d'attente extrait ou par défaut
    match = re.search(r"Wait (\d+) seconds", msg)
    wait_time = int(match.group(1)) if match else 60

    # Affichage barre de progression propre
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Attente avant prochaine commande...", total=wait_time)
            for _ in range(wait_time):
                await asyncio.sleep(1)
                progress.update(task, advance=1)
    except Exception as e:
        console.print(f"[bold red]Erreur durant l'attente :[/bold red] {e}")

    # Renvoi de la commande
    try:
        await client.send_message(bot_username, "✅ Free Bnb Collect 🎰")
        console.print("[bold green]Commande envoyée avec succès.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Erreur lors de l'envoi :[/bold red] {e}")

async def main():
    try:
        await client.start(phone=phone)
        console.print("[bold yellow]Bot démarré...[/bold yellow]")

        try:
            await client.get_entity(bot_username)
        except ValueError:
            console.print(f"[bold red]Erreur : le bot @{bot_username} est introuvable.[/bold red]")
            return

        await client.send_message(bot_username, "✅ Free Bnb Collect 🎰")
        await client.run_until_disconnected()

    except Exception as e:
        console.print(f"[bold red]Erreur lors du démarrage :[/bold red] {e}")

with client:
    client.loop.run_until_complete(main())
