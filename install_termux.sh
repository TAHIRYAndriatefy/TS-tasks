#!/data/data/com.termux/files/usr/bin/bash

# Couleurs
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[•] Mise à jour de Termux...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[•] Installation des paquets requis...${NC}"
pkg install python git clang -y
pip install --upgrade pip
pip install telethon rich nuitka

# Installation de shc pour compiler les .sh
apt install -y shc

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

# Création du lanceur bnbbot
cat > bnbbot <<EOF
#!/data/data/com.termux/files/usr/bin/bash
cd \$HOME/TS-tasks
./bnb_collector_bin/main
EOF

chmod +x bnbbot
mv bnbbot /data/data/com.termux/files/usr/bin/

# Déplacement des fichiers de contrôle
[ -f "bnbbot-disable" ] && mv bnbbot-disable /data/data/com.termux/files/usr/bin/
[ -f "bnbbot-enable" ] && mv bnbbot-enable /data/data/com.termux/files/usr/bin/
chmod +x /data/data/com.termux/files/usr/bin/bnbbot-*

# Ajout au démarrage automatique si non présent
if ! grep -q "bnbbot" ~/.bashrc; then
  echo "bnbbot" >> ~/.bashrc
fi

echo -e "${YELLOW}[•] Compilation des fichiers Python...${NC}"
for pyfile in *.py; do
    [ -f "$pyfile" ] || continue
    name="${pyfile%.py}"
    nuitka --standalone --follow-imports --remove-output "$pyfile"
    mv "$name".dist "$name"_bin
    rm -rf "$pyfile" "$name".build "$name".dist
    echo -e "   -> $pyfile compilé."
done

echo -e "${YELLOW}[•] Compilation des fichiers shell (.sh, bnb_enable, bnb_disable)...${NC}"
for shfile in *.sh bnb_enable bnb_disable; do
    [ -f "$shfile" ] || continue
    shc -f "$shfile"
    mv "$shfile".x "$shfile"_bin
    rm -f "$shfile" "$shfile".x.c
    echo -e "   -> $shfile compilé."
done

# Sécurisation des fichiers compilés
chmod 555 *_bin || true
chmod 444 config.json *.log *.session 2>/dev/null

echo -e "${GREEN}[✓] Tous les fichiers sont compilés et protégés.${NC}"
echo -e "${YELLOW}[!] Le bot se lancera automatiquement au prochain démarrage de Termux.${NC}"

echo -e "${GREEN}Mahandrasa kely fa mandefa ilay script manaraka izaho${NC}"
read -p "TSINDRIO NY TOUCHE ENTRÉE"
clear

bash start.sh 2>/dev/null
