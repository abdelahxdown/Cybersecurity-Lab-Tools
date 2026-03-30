#!/bin/bash

# Petit script pour mon labo Proxmox : Bannissement auto des brute-force SSH
# Auteur: Abdellah Yahyaoui

LOG="/var/log/auth.log"
LIMIT=5
BANNED_LOG="/var/log/banned_ips.log"

# Check root
[[ $EUID -ne 0 ]] && echo "Lance le script en root !" && exit 1

echo "[i] Scan des logs en cours..."

# On cherche les échecs, on compte par IP et on bannit si ça dépasse la limite
grep "Failed password" "$LOG" | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr | while read count ip; do
    
    if [ "$count" -ge "$LIMIT" ]; then
        # On vérifie si l'IP est déjà dans iptables pour pas spammer les règles
        if ! iptables -L INPUT -v -n | grep -q "$ip"; then
            echo "[!] Brute-force : $ip ($count tentatives). Bannissement..."
            iptables -A INPUT -s "$ip" -j DROP
            echo "$(date) - BANNED: $ip ($count fails)" >> "$BANNED_LOG"
        fi
    fi
done

echo "[OK] Scan fini."
