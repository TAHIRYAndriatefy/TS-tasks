
# TS-tasks

TS-tasks dia projet Telegram bot ahafahana mahazo vola amin'ny alalan'ny fanaovana tâches (actions) sy fanaraha-maso automatique

# page facebook

https://www.facebook.com/profile.php?id=61553657020034.

## Fonctionnalités

- Collecte automatique de BNB via un bot Telegram
- Système d'installation simplifié sur Termux
- Fichier de configuration sécurisé (`config.json`)
- Système de mise à jour automatique via `majc`
- Lancement automatique du bot avec `bnbbot`
- Interface en ligne de commande stylisée avec couleurs
- Intégration cron pour exécution périodique
- Support mode clair/sombre (dans l'interface utilisateur Web à venir)

## Installation (sur Termux)

```bash
pkg update -y && pkg upgrade -y
pkg install git -y
git clone https://github.com/TAHIRYAndriatefy/TS-tasks.git
cd TS-tasks
bash install.sh
