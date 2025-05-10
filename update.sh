#!/data/data/com.termux/files/usr/bin/bash

echo "Stash des modifications locales..."
git stash

echo "Mise à jour depuis GitHub..."
git pull origin main

echo "Restauration des modifications locales..."
git stash pop

echo "Mise à jour terminée avec succès."
