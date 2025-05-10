#!/data/data/com.termux/files/usr/bnb_collector.sh_bin/bin/bash

# Couleurs
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

# Nettoyage
clear

# Logo ASCII
echo -e "${CYAN}"
echo "╔═══════════════════════════════════╗"
echo "║        BNB Collector BOT          ║"
echo "╠═══════════════════════════════════╣"
echo "║   Made by Tahiry Andriatefy       ║"
echo "╚═══════════════════════════════════╝"
sleep 1

# Animation de chargement
echo -e "${YELLOW}\nChargement..."
for i in {1..30}; do
  echo -n "#"
  sleep 0.03
done
echo -e "\n"

# Vérifie si Python est installé
if ! command -v python >/dev/null 2>&1; then
    echo -e "${RED}Python n'est pas installé. Installation...${NC}"
    pkg install python -y
fi

# Menu interactif
while true; do
  echo -e "${CYAN}"
  echo "===== MENU ====="
  echo "1. Lancer le bot"
  echo "2. Activer le bot (bnbbot-enable)"
  echo "3. Désactiver le bot (bnbbot-disable)"
  echo "4. Quitter"
  echo -ne "${YELLOW}Choix : ${NC}"
  read choix

  case $choix in
    1)
      echo -e "${GREEN}Lancement de bnb_collector.py...${NC}"
     install_termux.sh_bin/python bnb_collector.py
      ;;
    2)
      echo -e "${GREEN}Activation du bot...${NC}"
      ./bnbbot-enable
      ;;
    3)
      echo -e "${RED}Désactivation du bot...${NC}"
      ./bnbbot-disable
      ;;
    4)
      echo -e "${YELLOW}Fermeture du menu. À bientôt !${NC}"
      exit
      ;;
    *)
      echo -e "${RED}Choix invalide.${NC}"
      ;;
  esac
done
