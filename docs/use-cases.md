# Cas d'Usage Spécifiques en Forensique Windows

## Insider Threats - Menaces internes

### Vue d'ensemble des menaces internes

Les menaces internes représentent l'un des défis les plus complexes en cybersécurité, impliquant des individus ayant un accès légitime aux systèmes d'une organisation.

#### Types de menaces internes

**Menaces malveillantes**
- Employés mécontents
- Espionnage industriel
- Sabotage informatique
- Vol d'informations sensibles

**Menaces non-intentionnelles**
- Négligence des employés
- Erreurs de configuration
- Violation involontaire de politiques
- Compromission d'identifiants

**Menaces compromises**
- Comptes utilisateurs compromis
- Élévation de privilèges
- Mouvements latéraux
- Persistance avancée

### Détection d'activités suspectes

#### Indicateurs comportementaux

**Analyse des patterns d'accès**
```powershell
# Analyser les connexions hors heures normales
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4624} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $logonTime = $_.TimeCreated
    $userName = ($eventData | Where-Object {$_.Name -eq "TargetUserName"}).'#text'
    $logonType = ($eventData | Where-Object {$_.Name -eq "LogonType"}).'#text'
    $sourceIP = ($eventData | Where-Object {$_.Name -eq "IpAddress"}).'#text'
    
    # Identifier les connexions hors heures (weekends, nuits)
    $isWeekend = $logonTime.DayOfWeek -in @([System.DayOfWeek]::Saturday, [System.DayOfWeek]::Sunday)
    $isNight = $logonTime.Hour -lt 6 -or $logonTime.Hour -gt 22
    
    if ($isWeekend -or $isNight) {
        [PSCustomObject]@{
            TimeCreated = $logonTime
            UserName = $userName
            LogonType = $logonType
            SourceIP = $sourceIP
            Anomaly = if ($isWeekend) { "Weekend Access" } else { "Night Access" }
        }
    }
} | Where-Object {$_.UserName -ne "SYSTEM" -and $_.UserName -ne ""}
```

**Détection d'accès aux données sensibles**
```powershell
# Monitoring des accès aux fichiers sensibles
function Monitor-SensitiveFileAccess {
    param(
        [string[]]$SensitivePaths = @(
            "C:\Sensitive\",
            "C:\HR\",
            "C:\Finance\",
            "C:\Confidential\"
        )
    )
    
    Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4663} | ForEach-Object {
        $event = [xml]$_.ToXml()
        $eventData = $event.Event.EventData.Data
        
        $objectName = ($eventData | Where-Object {$_.Name -eq "ObjectName"}).'#text'
        $subjectUser = ($eventData | Where-Object {$_.Name -eq "SubjectUserName"}).'#text'
        $accessMask = ($eventData | Where-Object {$_.Name -eq "AccessMask"}).'#text'
        $processName = ($eventData | Where-Object {$_.Name -eq "ProcessName"}).'#text'
        
        foreach ($path in $SensitivePaths) {
            if ($objectName -like "$path*") {
                [PSCustomObject]@{
                    TimeCreated = $_.TimeCreated
                    UserName = $subjectUser
                    ObjectName = $objectName
                    AccessMask = $accessMask
                    ProcessName = $processName
                    SensitiveArea = $path
                }
            }
        }
    }
}
```

#### Analyse des comportements utilisateur

**Profiling des utilisateurs**
```python
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

def create_user_behavior_profile(user_events):
    """
    Créer un profil comportemental d'utilisateur
    """
    
    # Convertir en DataFrame
    df = pd.DataFrame(user_events)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extraire les features comportementales
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6])
    
    # Calculer les statistiques
    profile = {
        'user_id': df['user_id'].iloc[0],
        'total_events': len(df),
        'unique_machines': df['machine'].nunique(),
        'unique_processes': df['process'].nunique(),
        'avg_session_duration': df.groupby('session_id')['timestamp'].apply(
            lambda x: (x.max() - x.min()).total_seconds()
        ).mean(),
        'common_hours': df['hour'].value_counts().head(3).index.tolist(),
        'weekend_activity_ratio': df['is_weekend'].mean(),
        'failed_logons': len(df[df['event_type'] == 'failed_logon']),
        'file_access_count': len(df[df['event_type'] == 'file_access']),
        'network_connections': len(df[df['event_type'] == 'network_connection'])
    }
    
    return profile

def detect_behavioral_anomalies(current_profile, historical_profiles):
    """
    Détecter les anomalies comportementales
    """
    
    # Préparer les données pour l'analyse
    features = ['unique_machines', 'unique_processes', 'avg_session_duration',
                'weekend_activity_ratio', 'failed_logons', 'file_access_count',
                'network_connections']
    
    # Créer la matrice de features
    historical_data = []
    for profile in historical_profiles:
        historical_data.append([profile[feature] for feature in features])
    
    current_data = [current_profile[feature] for feature in features]
    
    # Utiliser Isolation Forest pour détecter les anomalies
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    iso_forest.fit(historical_data)
    
    # Prédire si le comportement actuel est anormal
    anomaly_score = iso_forest.decision_function([current_data])[0]
    is_anomaly = iso_forest.predict([current_data])[0] == -1
    
    return {
        'is_anomaly': is_anomaly,
        'anomaly_score': anomaly_score,
        'threshold': iso_forest.threshold_
    }
```

### Corrélation multi-sources

#### Intégration des données

**Corrélation Active Directory et fichiers**
```powershell
function Correlate-ADAndFileAccess {
    param(
        [datetime]$StartTime,
        [datetime]$EndTime,
        [string]$TargetUser
    )
    
    # Récupérer les événements AD
    $adEvents = Get-WinEvent -FilterHashtable @{
        LogName="Security"
        Id=4624,4625,4768,4769,4770
        StartTime=$StartTime
        EndTime=$EndTime
    } | Where-Object {
        $event = [xml]$_.ToXml()
        $userName = ($event.Event.EventData.Data | Where-Object {$_.Name -eq "TargetUserName"}).'#text'
        $userName -eq $TargetUser
    }
    
    # Récupérer les accès fichiers
    $fileEvents = Get-WinEvent -FilterHashtable @{
        LogName="Security"
        Id=4656,4658,4663
        StartTime=$StartTime
        EndTime=$EndTime
    } | Where-Object {
        $event = [xml]$_.ToXml()
        $userName = ($event.Event.EventData.Data | Where-Object {$_.Name -eq "SubjectUserName"}).'#text'
        $userName -eq $TargetUser
    }
    
    # Récupérer les événements Sysmon
    $sysmonEvents = Get-WinEvent -FilterHashtable @{
        LogName="Microsoft-Windows-Sysmon/Operational"
        Id=1,3,11
        StartTime=$StartTime
        EndTime=$EndTime
    } | Where-Object {
        $event = [xml]$_.ToXml()
        $userName = ($event.Event.EventData.Data | Where-Object {$_.Name -eq "User"}).'#text'
        $userName -like "*$TargetUser*"
    }
    
    # Corréler les événements
    $correlatedEvents = @()
    
    foreach ($adEvent in $adEvents) {
        $adTime = $adEvent.TimeCreated
        
        # Trouver les événements fichiers dans une fenêtre de 5 minutes
        $relatedFileEvents = $fileEvents | Where-Object {
            $timeDiff = [math]::Abs(($_.TimeCreated - $adTime).TotalMinutes)
            $timeDiff -le 5
        }
        
        # Trouver les événements Sysmon dans une fenêtre de 5 minutes
        $relatedSysmonEvents = $sysmonEvents | Where-Object {
            $timeDiff = [math]::Abs(($_.TimeCreated - $adTime).TotalMinutes)
            $timeDiff -le 5
        }
        
        if ($relatedFileEvents -or $relatedSysmonEvents) {
            $correlatedEvents += [PSCustomObject]@{
                ADEvent = $adEvent
                RelatedFileEvents = $relatedFileEvents
                RelatedSysmonEvents = $relatedSysmonEvents
                TimeWindow = $adTime
            }
        }
    }
    
    return $correlatedEvents
}
```

### Cas d'études pratiques

#### Cas d'étude 1: Vol de données par employé

**Scénario**
Un employé du département IT télécharge massivement des fichiers confidentiels avant son départ.

**Analyse forensique**
```powershell
# 1. Analyser les accès aux fichiers sensibles
$suspiciousFileAccess = Get-WinEvent -FilterHashtable @{
    LogName="Security"
    Id=4663
    StartTime=(Get-Date).AddDays(-30)
} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $objectName = ($eventData | Where-Object {$_.Name -eq "ObjectName"}).'#text'
    $subjectUser = ($eventData | Where-Object {$_.Name -eq "SubjectUserName"}).'#text'
    
    if ($objectName -like "*Confidential*" -or $objectName -like "*HR*") {
        [PSCustomObject]@{
            TimeCreated = $_.TimeCreated
            UserName = $subjectUser
            FileName = $objectName
            Action = "File Access"
        }
    }
} | Group-Object UserName | Sort-Object Count -Descending

# 2. Analyser les téléchargements
$downloadEvents = Get-WinEvent -FilterHashtable @{
    LogName="Microsoft-Windows-Sysmon/Operational"
    Id=11
    StartTime=(Get-Date).AddDays(-30)
} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $targetFilename = ($eventData | Where-Object {$_.Name -eq "TargetFilename"}).'#text'
    $user = ($eventData | Where-Object {$_.Name -eq "User"}).'#text'
    
    if ($targetFilename -like "*Downloads*" -or $targetFilename -like "*USB*") {
        [PSCustomObject]@{
            TimeCreated = $_.TimeCreated
            UserName = $user
            FileName = $targetFilename
            Action = "File Creation"
        }
    }
}

# 3. Corréler avec les connexions USB
$usbEvents = Get-WinEvent -FilterHashtable @{
    LogName="System"
    Id=20001,20003
    StartTime=(Get-Date).AddDays(-30)
}
```

#### Cas d'étude 2: Sabotage système

**Scénario**
Un administrateur système supprime des fichiers critiques et modifie des configurations.

**Analyse forensique**
```powershell
# 1. Analyser les suppressions de fichiers
$deletionEvents = Get-WinEvent -FilterHashtable @{
    LogName="Security"
    Id=4660,4663
    StartTime=(Get-Date).AddDays(-7)
} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $objectName = ($eventData | Where-Object {$_.Name -eq "ObjectName"}).'#text'
    $subjectUser = ($eventData | Where-Object {$_.Name -eq "SubjectUserName"}).'#text'
    $accessMask = ($eventData | Where-Object {$_.Name -eq "AccessMask"}).'#text'
    
    # AccessMask 0x10000 = DELETE
    if ($accessMask -eq "0x10000") {
        [PSCustomObject]@{
            TimeCreated = $_.TimeCreated
            UserName = $subjectUser
            ObjectName = $objectName
            Action = "File Deletion"
        }
    }
}

# 2. Analyser les modifications de registre
$registryEvents = Get-WinEvent -FilterHashtable @{
    LogName="Security"
    Id=4657
    StartTime=(Get-Date).AddDays(-7)
} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $objectName = ($eventData | Where-Object {$_.Name -eq "ObjectName"}).'#text'
    $subjectUser = ($eventData | Where-Object {$_.Name -eq "SubjectUserName"}).'#text'
    
    if ($objectName -like "*Services*" -or $objectName -like "*Policies*") {
        [PSCustomObject]@{
            TimeCreated = $_.TimeCreated
            UserName = $subjectUser
            RegistryKey = $objectName
            Action = "Registry Modification"
        }
    }
}
```

## APT Detection - Menaces persistantes avancées

### Vue d'ensemble des APT

Les Advanced Persistent Threats (APT) sont des campagnes d'attaque sophistiquées et persistantes, généralement menées par des acteurs étatiques ou des groupes criminels organisés.

#### Caractéristiques des APT

**Sophistication technique**
- Outils personnalisés
- Techniques d'évasion avancées
- Exploitation de zero-days
- Chiffrement des communications

**Persistance**
- Présence à long terme
- Multiples mécanismes de persistance
- Redondance des accès
- Capacité de récupération

**Discrétion**
- Activité minimale
- Camouflage dans le trafic légitime
- Suppression des traces
- Techniques anti-forensiques

### Techniques d'APT

#### Vecteurs d'attaque courants

**Spear Phishing**
```powershell
# Détection d'emails de spear phishing
function Detect-SpearPhishing {
    param([string]$MailboxPath)
    
    # Analyser les emails avec pièces jointes suspectes
    $suspiciousEmails = Get-ChildItem -Path $MailboxPath -Recurse -Include "*.eml" | ForEach-Object {
        $email = Get-Content $_.FullName -Raw
        
        # Indicateurs de spear phishing
        $indicators = @(
            "urgent.*action.*required",
            "click.*here.*immediately",
            "verify.*account.*information",
            "suspended.*account",
            "unusual.*activity"
        )
        
        $attachmentTypes = @("\.exe", "\.scr", "\.bat", "\.vbs", "\.js")
        
        $suspiciousIndicators = $indicators | Where-Object { $email -match $_ }
        $suspiciousAttachments = $attachmentTypes | Where-Object { $email -match $_ }
        
        if ($suspiciousIndicators -or $suspiciousAttachments) {
            [PSCustomObject]@{
                FilePath = $_.FullName
                SuspiciousIndicators = $suspiciousIndicators
                SuspiciousAttachments = $suspiciousAttachments
                Email = $email
            }
        }
    }
    
    return $suspiciousEmails
}
```

**Watering Hole Attacks**
```powershell
# Analyser l'historique de navigation pour détecter les watering holes
function Detect-WateringHole {
    param([string]$BrowserHistoryPath)
    
    # Domaines suspects connus
    $suspiciousDomains = @(
        "suspicious-domain.com",
        "fake-news-site.org",
        "malicious-update.net"
    )
    
    # Analyser l'historique Chrome
    $chromeHistory = Invoke-SqliteQuery -DataSource "$BrowserHistoryPath\History" -Query "
        SELECT url, title, visit_count, last_visit_time 
        FROM urls 
        WHERE last_visit_time > datetime('now', '-30 days')
    "
    
    $suspiciousVisits = $chromeHistory | Where-Object {
        $url = $_.url
        $suspiciousDomains | Where-Object { $url -like "*$_*" }
    }
    
    return $suspiciousVisits
}
```

#### Techniques de mouvement latéral

**Pass-the-Hash Detection**
```powershell
# Détecter les attaques Pass-the-Hash
function Detect-PassTheHash {
    param(
        [datetime]$StartTime = (Get-Date).AddDays(-1),
        [datetime]$EndTime = (Get-Date)
    )
    
    # Événements de logon Type 3 (Network) avec NTLM
    $networkLogons = Get-WinEvent -FilterHashtable @{
        LogName="Security"
        Id=4624
        StartTime=$StartTime
        EndTime=$EndTime
    } | ForEach-Object {
        $event = [xml]$_.ToXml()
        $eventData = $event.Event.EventData.Data
        
        $logonType = ($eventData | Where-Object {$_.Name -eq "LogonType"}).'#text'
        $authPackage = ($eventData | Where-Object {$_.Name -eq "AuthenticationPackageName"}).'#text'
        $targetUser = ($eventData | Where-Object {$_.Name -eq "TargetUserName"}).'#text'
        $sourceIP = ($eventData | Where-Object {$_.Name -eq "IpAddress"}).'#text'
        $logonProcess = ($eventData | Where-Object {$_.Name -eq "LogonProcessName"}).'#text'
        
        if ($logonType -eq "3" -and $authPackage -eq "NTLM") {
            [PSCustomObject]@{
                TimeCreated = $_.TimeCreated
                TargetUser = $targetUser
                SourceIP = $sourceIP
                LogonProcess = $logonProcess
                AuthPackage = $authPackage
                LogonType = $logonType
            }
        }
    }
    
    # Identifier les patterns suspects
    $suspiciousLogons = $networkLogons | Group-Object TargetUser | Where-Object {
        $_.Count -gt 10  # Nombreuses connexions
    } | ForEach-Object {
        $userLogons = $_.Group
        $uniqueIPs = $userLogons | Group-Object SourceIP
        
        if ($uniqueIPs.Count -gt 5) {  # Depuis plusieurs IPs
            [PSCustomObject]@{
                UserName = $_.Name
                LogonCount = $_.Count
                UniqueIPs = $uniqueIPs.Count
                FirstLogon = ($userLogons | Sort-Object TimeCreated)[0].TimeCreated
                LastLogon = ($userLogons | Sort-Object TimeCreated)[-1].TimeCreated
                SourceIPs = $uniqueIPs.Name
            }
        }
    }
    
    return $suspiciousLogons
}
```

### Détection d'activités APT

#### Analyse des communications C2

**Détection de beaconing**
```python
import pandas as pd
import numpy as np
from collections import defaultdict

def detect_c2_beaconing(network_logs):
    """
    Détecter les communications de beaconing C2
    """
    
    # Analyser les connexions par destination
    connections = defaultdict(list)
    
    for log in network_logs:
        key = f"{log['src_ip']}->{log['dst_ip']}:{log['dst_port']}"
        connections[key].append(log['timestamp'])
    
    beacons = []
    
    for connection, timestamps in connections.items():
        if len(timestamps) < 10:  # Minimum 10 connexions
            continue
            
        # Calculer les intervalles
        timestamps.sort()
        intervals = []
        
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds()
            intervals.append(interval)
        
        if len(intervals) < 5:
            continue
            
        # Analyser la régularité
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        cv = std_interval / mean_interval if mean_interval > 0 else 0
        
        # Coefficient de variation faible = beaconing
        if cv < 0.3 and mean_interval > 60:  # CV < 30% et intervalle > 1min
            beacons.append({
                'connection': connection,
                'count': len(timestamps),
                'mean_interval': mean_interval,
                'std_interval': std_interval,
                'cv': cv,
                'first_seen': timestamps[0],
                'last_seen': timestamps[-1]
            })
    
    return beacons
```

**Détection de DNS tunneling**
```python
def detect_dns_tunneling(dns_logs):
    """
    Détecter le tunneling DNS
    """
    
    suspicious_domains = []
    
    # Analyser les requêtes DNS
    for log in dns_logs:
        domain = log['query_name']
        
        # Indicateurs de tunneling
        indicators = {
            'long_subdomain': len(domain.split('.')[0]) > 50,
            'high_entropy': calculate_entropy(domain) > 4.5,
            'unusual_tld': domain.split('.')[-1] in ['tk', 'ml', 'ga', 'cf'],
            'base64_like': is_base64_like(domain.split('.')[0]),
            'hex_like': is_hex_like(domain.split('.')[0])
        }
        
        suspicion_score = sum(indicators.values())
        
        if suspicion_score >= 2:
            suspicious_domains.append({
                'domain': domain,
                'timestamp': log['timestamp'],
                'client_ip': log['client_ip'],
                'indicators': indicators,
                'suspicion_score': suspicion_score
            })
    
    return suspicious_domains

def calculate_entropy(string):
    """Calculer l'entropie d'une chaîne"""
    import math
    from collections import Counter
    
    counter = Counter(string)
    length = len(string)
    entropy = 0
    
    for count in counter.values():
        p = count / length
        entropy -= p * math.log2(p)
    
    return entropy
```

### Analyse de campagnes

#### Attribution et profiling

**Analyse des TTPs (Tactics, Techniques, Procedures)**
```python
def analyze_apt_ttps(incident_data):
    """
    Analyser les TTPs d'un incident APT
    """
    
    # Mapping MITRE ATT&CK
    mitre_mapping = {
        'T1566': 'Phishing',
        'T1078': 'Valid Accounts',
        'T1055': 'Process Injection',
        'T1068': 'Exploitation for Privilege Escalation',
        'T1012': 'Query Registry',
        'T1083': 'File and Directory Discovery',
        'T1057': 'Process Discovery',
        'T1018': 'Remote System Discovery',
        'T1021': 'Remote Services',
        'T1105': 'Ingress Tool Transfer',
        'T1041': 'Exfiltration Over C2 Channel',
        'T1027': 'Obfuscated Files or Information'
    }
    
    detected_ttps = []
    
    for evidence in incident_data:
        # Analyser les artefacts pour identifier les TTPs
        if 'email' in evidence['type']:
            if any(indicator in evidence['content'] for indicator in ['urgent', 'click here', 'verify']):
                detected_ttps.append('T1566')
        
        if 'process' in evidence['type']:
            if any(technique in evidence['command_line'] for technique in ['powershell', 'rundll32', 'regsvr32']):
                detected_ttps.append('T1055')
        
        if 'registry' in evidence['type']:
            detected_ttps.append('T1012')
        
        if 'network' in evidence['type']:
            if evidence['protocol'] == 'DNS' and len(evidence['query']) > 50:
                detected_ttps.append('T1041')
    
    # Créer le profil TTP
    ttp_profile = {
        'detected_ttps': list(set(detected_ttps)),
        'ttp_descriptions': {ttp: mitre_mapping.get(ttp, 'Unknown') for ttp in detected_ttps},
        'attack_phases': categorize_attack_phases(detected_ttps),
        'sophistication_score': calculate_sophistication_score(detected_ttps)
    }
    
    return ttp_profile
```

## Ransomware Analysis - Analyse de rançongiciels

### Vue d'ensemble des ransomwares

Les ransomwares représentent une menace majeure, chiffrant les données des victimes et exigeant une rançon pour leur récupération.

#### Types de ransomware

**Crypto-ransomware**
- Chiffrement des fichiers utilisateur
- Demande de rançon en cryptocurrency
- Exemples: WannaCry, Ryuk, Conti

**Locker-ransomware**
- Verrouillage de l'interface utilisateur
- Blocage de l'accès au système
- Moins courant actuellement

**Ransomware-as-a-Service (RaaS)**
- Modèle économique organisé
- Affiliation et partage des profits
- Exemples: Sodinokibi, DarkSide

### Détection précoce

#### Surveillance des comportements suspects

**Détection d'activité de chiffrement**
```powershell
# Surveiller les modifications massives de fichiers
function Monitor-FileEncryption {
    param([string[]]$MonitoredPaths)
    
    # Créer un FileSystemWatcher pour chaque chemin
    $watchers = @()
    
    foreach ($path in $MonitoredPaths) {
        $watcher = New-Object System.IO.FileSystemWatcher
        $watcher.Path = $path
        $watcher.Filter = "*.*"
        $watcher.IncludeSubdirectories = $true
        $watcher.EnableRaisingEvents = $true
        
        # Événements à surveiller
        $watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite -bor [System.IO.NotifyFilters]::FileName
        
        # Variables pour détecter l'activité massive
        $script:fileChanges = @()
        $script:alertThreshold = 100  # 100 fichiers en 60 secondes
        
        Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action {
            $script:fileChanges += @{
                Path = $Event.SourceEventArgs.FullPath
                Timestamp = Get-Date
                Action = "Modified"
            }
            
            # Nettoyer les événements anciens (> 60 secondes)
            $cutoffTime = (Get-Date).AddSeconds(-60)
            $script:fileChanges = $script:fileChanges | Where-Object { $_.Timestamp -gt $cutoffTime }
            
            # Vérifier le seuil d'alerte
            if ($script:fileChanges.Count -ge $script:alertThreshold) {
                Write-Warning "RANSOMWARE ALERT: $($script:fileChanges.Count) file changes detected in 60 seconds"
                
                # Analyser les extensions
                $extensions = $script:fileChanges | ForEach-Object { 
                    [System.IO.Path]::GetExtension($_.Path) 
                } | Group-Object | Sort-Object Count -Descending
                
                Write-Host "Most common extensions:"
                $extensions | Select-Object -First 5 | ForEach-Object {
                    Write-Host "  $($_.Name): $($_.Count) files"
                }
            }
        }
        
        $watchers += $watcher
    }
    
    return $watchers
}
```

**Détection d'extensions de fichiers malveillantes**
```powershell
# Détecter les extensions de ransomware connues
function Detect-RansomwareExtensions {
    param([string[]]$ScanPaths)
    
    $ransomwareExtensions = @(
        ".encrypt", ".locked", ".crypto", ".crypt", ".crinf", ".r5a", ".XRNT",
        ".XTBL", ".crypt", ".R16M01D05", ".pzdc", ".good", ".LOL!", ".OMG!",
        ".RDM", ".RRK", ".encryptedRSA", ".crjoker", ".EnCiPhErEd", ".LeChiffre",
        ".keybtc@inbox_com", ".0x0", ".bleep", ".1999", ".vault", ".HA3",
        ".toxcrypt", ".magic", ".SUPERCRYPT", ".CTBL", ".CTB2", ".locky",
        ".zepto", ".odin", ".shit", ".fuck", ".petra", ".purge", ".dharma",
        ".wallet", ".bitcrypt", ".howDecrypt", ".html", ".cerber", ".cerber2",
        ".cerber3", ".encrypt", ".R16M01D05", ".gcman", ".krab", ".nozelesn",
        ".noproblemwedecfiles", ".EnCiPhErEd", ".encrypted", ".FuckYourData",
        ".Whereisyourfiles", ".encrypted", ".ttt", ".micro", ".mp3", ".encrypted",
        ".VforVendetta", ".LockLock", ".encrypted", ".xolzsec", ".antihacker2017",
        ".bitstak", ".coinvault", ".pzdc"
    )
    
    $detectedFiles = @()
    
    foreach ($path in $ScanPaths) {
        $files = Get-ChildItem -Path $path -Recurse -ErrorAction SilentlyContinue
        
        foreach ($file in $files) {
            $extension = [System.IO.Path]::GetExtension($file.FullName).ToLower()
            
            if ($extension -in $ransomwareExtensions) {
                $detectedFiles += [PSCustomObject]@{
                    FilePath = $file.FullName
                    Extension = $extension
                    LastWriteTime = $file.LastWriteTime
                    Size = $file.Length
                }
            }
        }
    }
    
    return $detectedFiles
}
```

### Analyse post-infection

#### Analyse des artefacts

**Analyse des notes de rançon**
```powershell
function Analyze-RansomNotes {
    param([string[]]$SearchPaths)
    
    $ransomNotePatterns = @(
        "*.txt", "*.html", "*.hta", "*.bmp", "*.jpg", "*.png"
    )
    
    $ransomKeywords = @(
        "ransom", "bitcoin", "decrypt", "encrypted", "files", "payment",
        "instruction", "recovery", "restore", "unlock", "key", "private",
        "BTC", "cryptocurrency", "tor", "onion", "deadline", "timer"
    )
    
    $detectedNotes = @()
    
    foreach ($path in $SearchPaths) {
        foreach ($pattern in $ransomNotePatterns) {
            $files = Get-ChildItem -Path $path -Filter $pattern -Recurse -ErrorAction SilentlyContinue
            
            foreach ($file in $files) {
                try {
                    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
                    
                    if ($content) {
                        $matchedKeywords = $ransomKeywords | Where-Object { $content -match $_ }
                        
                        if ($matchedKeywords.Count -ge 3) {
                            $detectedNotes += [PSCustomObject]@{
                                FilePath = $file.FullName
                                FileName = $file.Name
                                Size = $file.Length
                                CreationTime = $file.CreationTime
                                LastWriteTime = $file.LastWriteTime
                                MatchedKeywords = $matchedKeywords
                                Content = $content
                            }
                        }
                    }
                } catch {
                    # Ignorer les erreurs de lecture
                }
            }
        }
    }
    
    return $detectedNotes
}
```

**Analyse des processus de chiffrement**
```powershell
# Analyser les processus suspects liés au chiffrement
function Analyze-EncryptionProcesses {
    param([string]$LogPath)
    
    $encryptionIndicators = @(
        "CryptEncrypt", "CryptDecrypt", "CryptCreateHash", "CryptHashData",
        "BCryptEncrypt", "BCryptDecrypt", "BCryptCreateHash",
        "AES", "RSA", "DES", "3DES", "Blowfish", "Twofish",
        "OpenSSL", "CryptoAPI", "cryptbase.dll", "bcrypt.dll"
    )
    
    # Analyser les événements Sysmon de création de processus
    $suspiciousProcesses = Get-WinEvent -FilterHashtable @{
        LogName="Microsoft-Windows-Sysmon/Operational"
        Id=1
    } | ForEach-Object {
        $event = [xml]$_.ToXml()
        $eventData = $event.Event.EventData.Data
        
        $processName = ($eventData | Where-Object {$_.Name -eq "Image"}).'#text'
        $commandLine = ($eventData | Where-Object {$_.Name -eq "CommandLine"}).'#text'
        $parentProcess = ($eventData | Where-Object {$_.Name -eq "ParentImage"}).'#text'
        
        $matchedIndicators = $encryptionIndicators | Where-Object {
            $commandLine -match $_ -or $processName -match $_
        }
        
        if ($matchedIndicators) {
            [PSCustomObject]@{
                TimeCreated = $_.TimeCreated
                ProcessName = $processName
                CommandLine = $commandLine
                ParentProcess = $parentProcess
                MatchedIndicators = $matchedIndicators
            }
        }
    }
    
    return $suspiciousProcesses
}
```

### Récupération de données

#### Techniques de récupération

**Volume Shadow Copies**
```powershell
# Vérifier et récupérer depuis les Volume Shadow Copies
function Recover-FromShadowCopies {
    param([string]$TargetPath)
    
    # Lister les shadow copies disponibles
    $shadowCopies = Get-WmiObject -Class Win32_ShadowCopy
    
    if ($shadowCopies.Count -eq 0) {
        Write-Warning "No shadow copies found"
        return
    }
    
    Write-Host "Available shadow copies:"
    $shadowCopies | ForEach-Object {
        Write-Host "  ID: $($_.ID)"
        Write-Host "  InstallDate: $($_.InstallDate)"
        Write-Host "  VolumeName: $($_.VolumeName)"
        Write-Host "---"
    }
    
    # Créer un lien symbolique vers la shadow copy la plus récente
    $latestShadow = $shadowCopies | Sort-Object InstallDate -Descending | Select-Object -First 1
    
    if ($latestShadow) {
        $shadowPath = $latestShadow.DeviceObject + "\"
        $linkPath = "C:\ShadowRecovery"
        
        # Créer le lien symbolique
        cmd /c "mklink /d $linkPath $shadowPath"
        
        Write-Host "Shadow copy linked to: $linkPath"
        Write-Host "You can now access files from: $linkPath$TargetPath"
    }
}
```

**Récupération de fichiers supprimés**
```powershell
# Utiliser des outils de récupération de fichiers
function Recover-DeletedFiles {
    param(
        [string]$DriveLetter,
        [string]$OutputPath
    )
    
    # Utiliser PhotoRec pour récupérer les fichiers
    $photorecPath = "C:\Tools\photorec.exe"
    
    if (Test-Path $photorecPath) {
        $photorecArgs = @(
            "/d", $OutputPath,
            "/cmd", $DriveLetter,
            "fileopt,everything,enable",
            "search"
        )
        
        Start-Process -FilePath $photorecPath -ArgumentList $photorecArgs -Wait
        
        Write-Host "File recovery completed. Check: $OutputPath"
    } else {
        Write-Warning "PhotoRec not found at: $photorecPath"
    }
}
```

### Prévention et mitigation

#### Mesures préventives

**Monitoring en temps réel**
```powershell
# Système de monitoring en temps réel
function Start-RansomwareMonitoring {
    param([string[]]$ProtectedPaths)
    
    # Créer un job en arrière-plan
    $job = Start-Job -ScriptBlock {
        param($paths)
        
        # Importer les fonctions nécessaires
        function Monitor-FileEncryption {
            # (Code de la fonction précédente)
        }
        
        function Detect-RansomwareExtensions {
            # (Code de la fonction précédente)
        }
        
        # Démarrer le monitoring
        $watchers = Monitor-FileEncryption -MonitoredPaths $paths
        
        # Boucle de monitoring
        while ($true) {
            Start-Sleep -Seconds 60
            
            # Vérifier les extensions suspectes
            $suspiciousFiles = Detect-RansomwareExtensions -ScanPaths $paths
            
            if ($suspiciousFiles.Count -gt 0) {
                Write-Warning "RANSOMWARE DETECTED: $($suspiciousFiles.Count) encrypted files found"
                
                # Actions d'urgence
                # 1. Isoler le système
                # 2. Arrêter les services critiques
                # 3. Alerter les administrateurs
                
                break
            }
        }
        
        # Nettoyer les watchers
        foreach ($watcher in $watchers) {
            $watcher.Dispose()
        }
        
    } -ArgumentList $ProtectedPaths
    
    return $job
}
```

Cette approche complète permet d'analyser efficacement les différents types de menaces et d'incidents dans un environnement Windows.