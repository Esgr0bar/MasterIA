# Acquisition et Préservation des Preuves Numériques

## Techniques d'Acquisition Disque - Imagerie forensique

### Vue d'ensemble de l'acquisition

L'acquisition forensique est le processus de création d'une copie bit à bit d'un support de stockage tout en préservant l'intégrité des données pour l'analyse.

#### Principes fondamentaux

**Règle d'or : Ne jamais travailler sur l'original**
- Toujours créer une image forensique
- Maintenir la chaîne de custody
- Documenter chaque étape
- Vérifier l'intégrité des données

**Types d'acquisition**
1. **Acquisition complète** : Copie bit à bit de tout le disque
2. **Acquisition logique** : Copie des fichiers et dossiers
3. **Acquisition sélective** : Copie de zones spécifiques

### Création d'images DD et E01

#### Format DD (Data Dump)

**Caractéristiques**
- Format RAW (copie bit à bit)
- Pas de compression
- Pas de métadonnées intégrées
- Compatible avec la plupart des outils

**Création d'image DD**
```bash
# Acquisition complète d'un disque
dd if=/dev/sda of=/evidence/case001_disk.dd bs=64K conv=noerror,sync

# Avec monitoring du progrès
dd if=/dev/sda of=/evidence/case001_disk.dd bs=64K conv=noerror,sync status=progress

# Acquisition avec dcfldd (version améliorée)
dcfldd if=/dev/sda of=/evidence/case001_disk.dd bs=64K hash=sha256 hashwindow=1G hashlog=/evidence/case001_disk.hash
```

**Paramètres importants**
- `bs=64K` : Taille des blocs pour optimiser la vitesse
- `conv=noerror,sync` : Continue en cas d'erreur et remplit avec des zéros
- `hash=sha256` : Calcul du hash pendant l'acquisition

#### Format E01 (Expert Witness)

**Caractéristiques**
- Format propriétaire d'EnCase
- Compression intégrée
- Métadonnées et checksums
- Support de la segmentation

**Création d'image E01**
```bash
# Avec ewfacquire (libewf)
ewfacquire -t /evidence/case001 -C case001 -D "Windows 10 workstation" -E "John Doe" -N "Investigation malware" -M removable -f encase6 -S 1.4GB /dev/sda

# Avec FTK Imager (ligne de commande)
ftkimager.exe /dev/sda /evidence/case001 --e01 --compress 6 --frag 1.4GB
```

**Métadonnées E01**
- Case Number
- Evidence Number
- Unique Description
- Examiner Name
- Notes
- Compression Level
- Sector Size

### Outils d'acquisition

#### FTK Imager

**Interface graphique**
1. **Add Evidence Item** → **Physical Drive**
2. Sélectionner le disque source
3. **Create Disk Image** → **E01**
4. Configurer les métadonnées
5. Démarrer l'acquisition

**Ligne de commande**
```cmd
# Acquisition complète
ftkimager.exe \\.\PhysicalDrive0 C:\Evidence\case001 --e01 --compress 6

# Acquisition avec vérification
ftkimager.exe \\.\PhysicalDrive0 C:\Evidence\case001 --e01 --verify

# Acquisition de partition logique
ftkimager.exe C: C:\Evidence\case001_C --e01
```

#### dd et variantes

**dd classique**
```bash
# Acquisition de base
dd if=/dev/sda of=/evidence/image.dd bs=64K

# Avec gestion d'erreurs
dd if=/dev/sda of=/evidence/image.dd bs=64K conv=noerror,sync

# Acquisition d'une partition
dd if=/dev/sda1 of=/evidence/partition.dd bs=64K
```

**dcfldd (amélioration de dd)**
```bash
# Acquisition avec hash
dcfldd if=/dev/sda of=/evidence/image.dd bs=64K hash=sha256 hashwindow=1G hashlog=/evidence/hash.log

# Acquisition avec split
dcfldd if=/dev/sda of=/evidence/image.dd bs=64K split=2G hash=sha256

# Acquisition avec wipe du destination
dcfldd if=/dev/sda of=/evidence/image.dd bs=64K wipe=/evidence/image.dd hash=sha256
```

**ddrescue (récupération avancée)**
```bash
# Acquisition avec mapfile de récupération
ddrescue -f -n /dev/sda /evidence/image.dd /evidence/mapfile.log

# Phase de récupération des secteurs endommagés
ddrescue -f -d -r3 /dev/sda /evidence/image.dd /evidence/mapfile.log

# Affichage du statut
ddrescue -f -n /dev/sda /evidence/image.dd /evidence/mapfile.log --verbose
```

### Vérification d'intégrité

#### Calcul des hash

**MD5 (déprécié mais encore utilisé)**
```bash
md5sum /evidence/image.dd > /evidence/image.dd.md5
```

**SHA-256 (recommandé)**
```bash
sha256sum /evidence/image.dd > /evidence/image.dd.sha256
```

**Vérification multiple**
```bash
# Calcul simultané de plusieurs hash
rhash --md5 --sha1 --sha256 /evidence/image.dd > /evidence/image.dd.hash
```

#### Checksums intégrés

**Vérification E01**
```bash
# Avec ewfverify
ewfverify /evidence/case001.E01

# Information sur l'image
ewfinfo /evidence/case001.E01
```

**Vérification DD**
```bash
# Comparaison hash
sha256sum -c /evidence/image.dd.sha256

# Vérification complète
cmp /dev/sda /evidence/image.dd
```

### Acquisition en live vs post-mortem

#### Acquisition Live

**Avantages**
- Capture de la mémoire volatile
- Processus en cours d'exécution
- Connexions réseau actives
- Données non chiffrées

**Inconvénients**
- Modification potentielle des données
- Instabilité du système
- Preuves volatiles

**Outils pour acquisition live**
```bash
# Acquisition mémoire avec LiME
insmod lime.ko "path=/evidence/memory.lime format=lime"

# Acquisition avec Volatility
python vol.py --profile=Win10x64 -f /evidence/memory.dump imageinfo

# Acquisition disque live
dd if=/dev/sda of=/evidence/live_image.dd bs=64K conv=noerror,sync
```

#### Acquisition Post-Mortem

**Avantages**
- Système stable
- Pas de modification des données
- Acquisition complète garantie

**Inconvénients**
- Perte des données volatiles
- Chiffrement potentiel
- Pas d'accès aux processus

**Méthode recommandée**
```bash
# Boot sur support externe (DEFT, CAINE, etc.)
# Acquisition complète
dcfldd if=/dev/sda of=/evidence/postmortem.dd bs=64K hash=sha256 hashwindow=1G

# Vérification
sha256sum /evidence/postmortem.dd > /evidence/postmortem.dd.sha256
```

## Préservation des Preuves - Chain of custody

### Méthodologie de collecte

#### Préparation

**Équipement nécessaire**
- Disques de stockage stérilisés
- Bloqueurs d'écriture (write blockers)
- Outils d'acquisition
- Équipement de documentation (appareil photo, étiquettes)

**Stérilisation des supports**
```bash
# Effacement sécurisé
shred -vfz -n 3 /dev/sdb

# Vérification
hexdump -C /dev/sdb | head -20
```

#### Procédure de collecte

**1. Sécurisation de la scène**
- Isoler le système
- Documenter l'état initial
- Photographier l'installation

**2. Acquisition des données volatiles**
```bash
# Processus en cours
ps aux > /evidence/processes.txt

# Connexions réseau
netstat -tulpn > /evidence/network.txt

# Utilisateurs connectés
w > /evidence/users.txt

# Modules kernel
lsmod > /evidence/modules.txt
```

**3. Acquisition des données persistantes**
```bash
# Image du disque système
dcfldd if=/dev/sda of=/evidence/system.dd bs=64K hash=sha256 hashwindow=1G hashlog=/evidence/system.hash

# Sauvegarde du registre (Windows)
reg save HKLM\SYSTEM /evidence/SYSTEM.hiv
reg save HKLM\SOFTWARE /evidence/SOFTWARE.hiv
reg save HKLM\SAM /evidence/SAM.hiv
```

### Documentation légale

#### Formulaire de chaîne de custody

**Informations requises**
- Date et heure
- Nom de l'enquêteur
- Description de la preuve
- Localisation de la collecte
- Méthode d'acquisition
- Hash de vérification
- Signature

**Modèle de documentation**
```
CHAIN OF CUSTODY FORM
Case Number: [CASE-2024-001]
Date: [2024-01-15]
Time: [14:30 UTC]
Investigator: [John Doe]
Item Description: [Dell Laptop - Windows 10]
Serial Number: [ABC123456]
Acquisition Method: [FTK Imager - E01 format]
Hash SHA256: [abcd1234...]
Storage Location: [Evidence Locker A-15]
Signature: [John Doe]
```

#### Métadonnées forensiques

**Informations système**
```bash
# Informations hardware
dmidecode > /evidence/hardware.txt

# Informations système
uname -a > /evidence/system_info.txt

# Horodatage
date -u > /evidence/timestamp.txt
```

**Informations réseau**
```bash
# Configuration réseau
ip addr show > /evidence/network_config.txt

# Table de routage
ip route show > /evidence/routing.txt

# Résolution DNS
cat /etc/resolv.conf > /evidence/dns.txt
```

### Stockage sécurisé

#### Environnement de stockage

**Exigences physiques**
- Température contrôlée (18-24°C)
- Humidité relative 45-65%
- Protection contre les champs magnétiques
- Accès restreint et surveillé

**Conteneurs**
- Sacs antistatiques
- Boîtes de Faraday
- Étiquetage clair
- Numérotation séquentielle

#### Chiffrement des preuves

**Chiffrement des images disque**
```bash
# Chiffrement avec GPG
gpg --symmetric --cipher-algo AES256 /evidence/image.dd

# Chiffrement avec LUKS
cryptsetup luksFormat /dev/sdb
cryptsetup luksOpen /dev/sdb evidence_encrypted
dd if=/evidence/image.dd of=/dev/mapper/evidence_encrypted
```

**Gestion des clés**
- Stockage séparé des clés
- Accès multi-personnes requis
- Audit des accès
- Sauvegarde sécurisée

### Standards et bonnes pratiques

#### Standards internationaux

**ISO 27037:2012**
- Lignes directrices pour l'identification, la collecte et la préservation
- Procédures de documentation
- Chaîne de custody

**NIST SP 800-86**
- Guide pour l'intégration de l'informatique forensique
- Recommandations techniques
- Procédures opérationnelles

#### Bonnes pratiques

**Validation des outils**
```bash
# Test avec données connues
dd if=/dev/zero of=/tmp/test.dd bs=1M count=100
sha256sum /tmp/test.dd > /tmp/test.sha256

# Acquisition de test
dcfldd if=/tmp/test.dd of=/tmp/test_copy.dd bs=64K hash=sha256
sha256sum -c /tmp/test.sha256
```

**Documentation continue**
- Journal détaillé des actions
- Horodatage précis
- Sauvegarde des logs
- Révision par pairs

**Procédures de qualité**
- Validation des outils
- Formation du personnel
- Audits réguliers
- Mise à jour des procédures

## Outils et techniques avancés

### Acquisition réseau

**Acquisition distante**
```bash
# Avec netcat
dd if=/dev/sda bs=64K | nc -l 4444

# Réception
nc target_ip 4444 | dd of=/evidence/remote_image.dd bs=64K
```

**Tunnel chiffré**
```bash
# Avec SSH
dd if=/dev/sda bs=64K | ssh user@forensic_server "dd of=/evidence/remote_image.dd bs=64K"
```

### Acquisition de supports spéciaux

**Disques SSD**
```bash
# Attention au TRIM
hdparm -I /dev/sda | grep TRIM

# Acquisition rapide recommandée
dcfldd if=/dev/sda of=/evidence/ssd.dd bs=64K hash=sha256
```

**Supports amovibles**
```bash
# Montage en lecture seule
mount -o ro /dev/sdb1 /mnt/usb

# Acquisition logique
tar -czf /evidence/usb_logical.tar.gz /mnt/usb/
```

Cette méthodologie d'acquisition et de préservation garantit l'intégrité des preuves numériques et leur recevabilité légale.