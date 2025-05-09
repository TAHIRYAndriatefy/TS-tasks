#!/bin/bash

# Couleurs
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Chemin vers le repo local
REPO_PATH="$HOME/TS-tasks-update"

# Nouvelle version demandée
read -p "Entrez la nouvelle version (ex: 1.3.1): " new_version

# Vérifie si le dossier existe
if [ ! -d "$REPO_PATH" ]; then
    echo -e "${YELLOW}[•] Clonage du dépôt GitHub...${NC}"
    git clone https://github.com/VOTRE_UTILISATEUR/TS-tasks-update.git "$REPO_PATH"
fi

cd "$REPO_PATH" || exit

# Met à jour le fichier version.txt
echo "$new_version" > version.txt

# Commit & push
git add version.txt
git commit -m "Mise à jour automatique à la version $new_version"
git push

echo -e "${GREEN}[✓] Version $new_version poussée avec succès sur GitHub.${NC}"
