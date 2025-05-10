#!/data/data/com.termux/files/usr/bin/bash

# Couleurs
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[•] Mise à jour de Termux...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[•] Installation des paquets requis...${NC}"
pkg install -y python git cronie
pip install --upgrade pip
pip install telethon rich

echo -e "${GREEN}[✓] Dépendances installées.${NC}"

# Lien API Telegram
termux-open-url "https://my.telegram.org"

echo -e "${YELLOW}[•] Connecte-toi à Telegram et crée une application.${NC}"
echo -e "${YELLOW}[•] Récupère ton API ID, API Hash et ton numéro de téléphone.${NC}"

read -p "API ID: " api_id
read -p "API HASH: " api_hash
read -p "Téléphone (+XXX...): " phone

# Création du fichier config.json
cat > config.json <<EOF
{
  "api_id": "$api_id",
  "api_hash": "$api_hash",
  "phone": "$phone"
}
EOF

echo -e "${GREEN}[✓] Fichier config.json généré.${NC}"

# Création des scripts de lancement
cat > majc <<EOF
#!/data/data/com.termux/files/usr/bin/bash
cd \$HOME/TS-tasks
./update.sh
EOF

cat > bnbbot <<EOF
#!/data/data/com.termux/files/usr/bin/bash
cd \$HOME/TS-tasks
python bnb_collector.py
EOF

chmod +x majc bnbbot
mv majc bnbbot /data/data/com.termux/files/usr/bin/

# Scripts facultatifs
[ -f "maj" ] && mv maj /data/data/com.termux/files/usr/bin/
[ -f "bnbbot-disable" ] && mv bnbbot-disable /data/data/com.termux/files/usr/bin/
[ -f "bnbbot-enable" ] && mv bnbbot-enable /data/data/com.termux/files/usr/bin/
chmod +x /data/data/com.termux/files/usr/bin/bnbbot*

# Ajout au démarrage automatique si non présent
if ! grep -q "maj" ~/.bashrc; then
  echo "maj" >> ~/.bashrc
fi
if ! grep -q "bnbbot" ~/.bashrc; then
  echo "bnbbot" >> ~/.bashrc
fi

echo -e "${GREEN}[✓] Installation terminée.${NC}"
echo -e "${YELLOW}[!] Le bot se lancera automatiquement au prochain démarrage de Termux.${NC}"

# Permissions
cd \$HOME/TS-tasks 2>/dev/null
chmod +x *.sh *.py

# Lancement
bash install-cron-update.sh 2>/dev/null

read -p "TSINDRIO NY TOUCHE ENTRÉE"
bash start.sh 2>/dev/null
clear
