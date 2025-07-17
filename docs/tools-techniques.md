# Outils et Techniques pour la Forensique Windows

## Autopsy et Sleuth Kit - Suite forensique open source

### Vue d'ensemble d'Autopsy

Autopsy est une interface graphique open source pour The Sleuth Kit (TSK), offrant une plateforme complète d'analyse forensique numérique.

#### Fonctionnalités principales

**Analyse d'images disque**
- Support des formats DD, E01, AFF
- Analyse des systèmes de fichiers
- Récupération de fichiers supprimés
- Analyse de la timeline

**Plugins intégrés**
- Hash lookup (NSRL, hashsets personnalisés)
- Keyword search
- Email analysis
- Registry analysis
- Web artifacts
- Multimedia file analysis

### Installation et configuration

#### Installation sur Windows

**Installation basique**
```bash
# Télécharger depuis https://www.autopsy.com/download/
# Installation standard avec installateur MSI

# Vérification de l'installation
autopsy --version
```

**Configuration initiale**
```bash
# Création d'un cas
autopsy --create-case "Case001" --case-dir "C:\Cases\Case001"

# Ajout d'une image
autopsy --add-data-source "C:\Evidence\disk.dd" --case-dir "C:\Cases\Case001"
```

#### Configuration avancée

**Configuration des index**
```properties
# autopsy.conf
index.enable=true
index.path=C:\AutopsyIndex
index.chunk.size=32
index.threads=4

# Configuration Solr
solr.server=localhost
solr.port=8983
solr.collection=autopsy
```

**Hashsets personnalisés**
```bash
# Création d'un hashset
sleuthkit_hash_db -d hashset.db create

# Ajout de hashs
sleuthkit_hash_db -d hashset.db add C:\hashs\malware_hashes.txt

# Configuration dans Autopsy
# Tools -> Options -> Global Hash Set Lookup
```

### Analyse d'images disque

#### Processus d'analyse

**Étapes d'analyse**
1. **Création du cas**
2. **Ajout des sources de données**
3. **Configuration des modules**
4. **Lancement de l'analyse**
5. **Examen des résultats**

**Script d'analyse automatisée**
```python
import pyautopsy

def automated_analysis(case_name, evidence_path):
    # Créer un nouveau cas
    case = pyautopsy.Case(case_name)
    
    # Ajouter l'image disque
    data_source = case.add_data_source(evidence_path)
    
    # Configurer les modules
    modules = [
        'Hash Lookup',
        'File Type Identification',
        'Keyword Search',
        'Email Parser',
        'Registry Analysis',
        'Web Artifacts',
        'Recent Activity',
        'Interesting Files'
    ]
    
    # Lancer l'analyse
    case.run_ingest(data_source, modules)
    
    # Attendre la fin de l'analyse
    case.wait_for_completion()
    
    # Générer un rapport
    report = case.generate_report()
    return report
```

#### Modules d'analyse

**Hash Lookup Module**
```python
# Configuration du module Hash Lookup
hash_config = {
    'nsrl_path': 'C:\\NSRL\\NSRLFile.txt',
    'custom_hashsets': [
        'C:\\Hashsets\\malware_hashes.db',
        'C:\\Hashsets\\known_good.db'
    ],
    'alert_on_no_hash': True,
    'calculate_md5': True,
    'calculate_sha1': True,
    'calculate_sha256': True
}
```

**Keyword Search Module**
```python
# Configuration des mots-clés
keyword_lists = {
    'malware_indicators': [
        'backdoor', 'trojan', 'virus', 'rootkit',
        'keylogger', 'botnet', 'payload', 'exploit'
    ],
    'network_indicators': [
        'http://', 'https://', 'ftp://', 'ssh://',
        'tcp://', 'udp://', 'smb://', 'rdp://'
    ],
    'password_related': [
        'password', 'passwd', 'pwd', 'login',
        'credentials', 'authentication', 'token'
    ],
    'crypto_indicators': [
        'bitcoin', 'cryptocurrency', 'wallet',
        'mining', 'ransomware', 'encryption'
    ]
}
```

### Corrélation d'artefacts

#### Analyse de timeline

**Création de timeline**
```python
def create_timeline(case_path, output_path):
    # Utiliser TSK pour créer une timeline
    import subprocess
    
    # Commande fls pour lister les fichiers
    fls_cmd = f"fls -r -m / {case_path} > {output_path}/bodyfile.txt"
    subprocess.run(fls_cmd, shell=True)
    
    # Commande mactime pour créer la timeline
    mactime_cmd = f"mactime -b {output_path}/bodyfile.txt -d > {output_path}/timeline.csv"
    subprocess.run(mactime_cmd, shell=True)
    
    return f"{output_path}/timeline.csv"
```

**Analyse de corrélation**
```python
def correlate_artifacts(case_path):
    correlations = {}
    
    # Corréler les artefacts web avec les fichiers téléchargés
    web_artifacts = get_web_artifacts(case_path)
    downloads = get_downloaded_files(case_path)
    
    for artifact in web_artifacts:
        for download in downloads:
            if abs((artifact.timestamp - download.timestamp).total_seconds()) < 300:
                correlations[artifact.url] = download.path
    
    # Corréler les processus avec les fichiers créés
    processes = get_process_artifacts(case_path)
    file_creations = get_file_creations(case_path)
    
    for process in processes:
        related_files = [f for f in file_creations 
                        if f.process_id == process.pid]
        if related_files:
            correlations[process.name] = related_files
    
    return correlations
```

### Génération de rapports

#### Rapport HTML

**Configuration du rapport**
```python
report_config = {
    'format': 'HTML',
    'include_data_sources': True,
    'include_results': True,
    'include_tags': True,
    'include_thumbnails': True,
    'output_path': 'C:\\Reports\\Case001_Report.html'
}
```

**Rapport personnalisé**
```python
def generate_custom_report(case_path, template_path):
    from jinja2 import Template
    
    # Charger le template
    with open(template_path, 'r') as f:
        template = Template(f.read())
    
    # Collecter les données
    data = {
        'case_name': get_case_name(case_path),
        'evidence_sources': get_evidence_sources(case_path),
        'artifacts': get_all_artifacts(case_path),
        'timeline': get_timeline_data(case_path),
        'correlations': correlate_artifacts(case_path)
    }
    
    # Générer le rapport
    report_html = template.render(data)
    
    # Sauvegarder
    with open('custom_report.html', 'w') as f:
        f.write(report_html)
    
    return 'custom_report.html'
```

## YARA Rules - Détection de patterns

### Vue d'ensemble de YARA

YARA est un outil de détection de patterns binaires et textuels, particulièrement utile pour la classification de malwares et l'analyse forensique.

#### Syntaxe de base

**Structure d'une règle YARA**
```yara
rule RuleName
{
    meta:
        description = "Description de la règle"
        author = "Nom de l'auteur"
        date = "2024-01-15"
        version = "1.0"
        
    strings:
        $string1 = "pattern à rechercher"
        $string2 = { 4D 5A }  // Hex pattern
        $regex1 = /pattern regex/
        
    condition:
        $string1 or $string2 or $regex1
}
```

### Création de règles YARA

#### Règles pour malwares

**Détection de packer UPX**
```yara
rule UPX_Packer
{
    meta:
        description = "Détection du packer UPX"
        author = "Forensic Analyst"
        date = "2024-01-15"
        
    strings:
        $upx1 = { 55 50 58 30 }  // UPX0
        $upx2 = { 55 50 58 31 }  // UPX1
        $upx3 = "UPX!"
        
    condition:
        uint16(0) == 0x5A4D and any of ($upx*)
}
```

**Détection de techniques d'injection**
```yara
rule Process_Injection
{
    meta:
        description = "Détection d'injection de processus"
        author = "Forensic Analyst"
        
    strings:
        $api1 = "CreateRemoteThread"
        $api2 = "VirtualAllocEx"
        $api3 = "WriteProcessMemory"
        $api4 = "OpenProcess"
        $api5 = "QueueUserAPC"
        
    condition:
        3 of ($api*)
}
```

**Détection de persistance**
```yara
rule Windows_Persistence
{
    meta:
        description = "Techniques de persistance Windows"
        
    strings:
        $reg1 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
        $reg2 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce"
        $reg3 = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon"
        $sched1 = "schtasks" nocase
        $sched2 = "at.exe" nocase
        $service1 = "sc create"
        $service2 = "CreateService"
        
    condition:
        any of ($reg*) or any of ($sched*) or any of ($service*)
}
```

#### Règles pour artefacts forensiques

**Détection d'activité PowerShell malveillante**
```yara
rule Malicious_PowerShell
{
    meta:
        description = "Détection de PowerShell malveillant"
        
    strings:
        $ps1 = "powershell.exe" nocase
        $ps2 = "powershell -e" nocase
        $ps3 = "powershell -enc" nocase
        $ps4 = "Invoke-Expression" nocase
        $ps5 = "IEX" nocase
        $ps6 = "DownloadString" nocase
        $ps7 = "Invoke-WebRequest" nocase
        $ps8 = "FromBase64String" nocase
        $obf1 = "char]" nocase
        $obf2 = "join" nocase
        $obf3 = "split" nocase
        
    condition:
        any of ($ps*) and any of ($obf*)
}
```

**Détection de traces de navigation**
```yara
rule Browser_Artifacts
{
    meta:
        description = "Artefacts de navigation web"
        
    strings:
        $chrome1 = "Google\\Chrome\\User Data"
        $chrome2 = "History"
        $chrome3 = "Cookies"
        $firefox1 = "Mozilla\\Firefox\\Profiles"
        $firefox2 = "places.sqlite"
        $firefox3 = "cookies.sqlite"
        $edge1 = "Microsoft\\Edge\\User Data"
        
    condition:
        any of ($chrome*) or any of ($firefox*) or any of ($edge*)
}
```

### Analyse de fichiers suspects

#### Scan de fichiers

**Scan basique**
```bash
# Scan d'un fichier
yara rules.yar suspicious_file.exe

# Scan d'un répertoire
yara -r rules.yar /path/to/directory

# Scan avec métadonnées
yara -m rules.yar suspicious_file.exe

# Scan avec tags
yara -t rules.yar suspicious_file.exe
```

**Scan avancé avec Python**
```python
import yara

def scan_with_yara(rules_path, target_path):
    # Compiler les règles
    rules = yara.compile(filepath=rules_path)
    
    # Scanner le fichier
    matches = rules.match(target_path)
    
    results = []
    for match in matches:
        result = {
            'rule': match.rule,
            'namespace': match.namespace,
            'tags': match.tags,
            'meta': match.meta,
            'strings': []
        }
        
        for string_match in match.strings:
            result['strings'].append({
                'identifier': string_match.identifier,
                'instances': string_match.instances
            })
        
        results.append(result)
    
    return results

# Utilisation
results = scan_with_yara('malware_rules.yar', 'suspicious_file.exe')
for result in results:
    print(f"Rule matched: {result['rule']}")
    print(f"Description: {result['meta'].get('description', 'N/A')}")
```

#### Analyse de mémoire

**Scan de dump mémoire**
```bash
# Scan d'un dump mémoire avec YARA
yara -s memory_rules.yar memory_dump.dmp

# Avec Volatility
volatility -f memory_dump.dmp --profile=Win10x64 yarascan -y malware_rules.yar
```

**Règles spécifiques à la mémoire**
```yara
rule Memory_Injection
{
    meta:
        description = "Détection d'injection en mémoire"
        
    strings:
        $mz = { 4D 5A }  // MZ header
        $pe = { 50 45 00 00 }  // PE header
        $inject1 = { 6A 00 68 00 30 00 00 68 00 00 40 00 6A 00 FF 15 }  // VirtualAllocEx pattern
        $inject2 = { 6A 00 6A 00 6A 04 6A 00 6A 00 68 00 00 40 00 }  // WriteProcessMemory pattern
        
    condition:
        $mz at 0 and $pe and any of ($inject*)
}
```

### Intégration avec d'autres outils

#### Intégration avec Autopsy

**Plugin YARA pour Autopsy**
```python
# autopsy_yara_plugin.py
import yara
from autopsy import IngestModule

class YaraIngestModule(IngestModule):
    def __init__(self):
        self.rules = None
        
    def startUp(self, context):
        # Charger les règles YARA
        self.rules = yara.compile(filepath='rules/all_rules.yar')
        
    def process(self, dataSource, progressBar):
        # Obtenir tous les fichiers
        files = dataSource.getFiles()
        
        for file in files:
            if file.isFile() and file.getSize() > 0:
                # Scanner le fichier
                try:
                    matches = self.rules.match(data=file.read())
                    
                    if matches:
                        # Créer un artefact
                        artifact = file.newArtifact(self.ARTIFACT_TYPE)
                        artifact.addAttribute(self.ATTR_RULE, matches[0].rule)
                        artifact.addAttribute(self.ATTR_DESCRIPTION, matches[0].meta.get('description', ''))
                        
                except Exception as e:
                    self.log(f"Error scanning file {file.getName()}: {e}")
        
        return IngestModule.ProcessResult.OK
```

#### Intégration avec Volatility

**Plugin Volatility YARA**
```python
# volatility_yara_plugin.py
import yara
import volatility.plugins.common as common
import volatility.utils as utils

class YaraScanPlugin(common.AbstractWindowsCommand):
    def __init__(self, config, *args, **kwargs):
        common.AbstractWindowsCommand.__init__(self, config, *args, **kwargs)
        
    def calculate(self):
        # Compiler les règles YARA
        rules = yara.compile(filepath=self._config.YARA_RULES)
        
        # Scanner l'espace d'adressage
        address_space = utils.load_as(self._config)
        
        for offset in range(0, address_space.get_available_addresses()):
            try:
                data = address_space.read(offset, 0x1000)  # Lire 4KB
                matches = rules.match(data=data)
                
                if matches:
                    yield (offset, matches)
                    
            except Exception:
                continue
    
    def render_text(self, outfd, data):
        for offset, matches in data:
            for match in matches:
                outfd.write(f"Rule: {match.rule} at offset 0x{offset:x}\n")
                outfd.write(f"Description: {match.meta.get('description', 'N/A')}\n")
```

### Optimisation des performances

#### Optimisation des règles

**Règles optimisées**
```yara
rule Optimized_Rule
{
    meta:
        description = "Règle optimisée pour les performances"
        
    strings:
        // Utiliser des patterns spécifiques au début
        $header = { 4D 5A ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 50 45 }
        
        // Éviter les patterns trop génériques
        $specific_string = "Very specific malware string"
        
        // Utiliser des modificateurs pour réduire les faux positifs
        $api_call = "CreateRemoteThread" nocase wide ascii
        
    condition:
        // Vérifier d'abord les patterns les plus spécifiques
        $header at 0 and ($specific_string or $api_call)
}
```

#### Configuration des performances

**Configuration YARA**
```yaml
# yara.conf
stack_size: 16384
max_strings_per_rule: 10000
max_match_length: 1000000

# Timeout pour les règles
timeout: 60

# Optimisations
fast_scan: true
disable_console_logs: true
```

## Timeline Analysis - Reconstruction temporelle

### Vue d'ensemble de l'analyse temporelle

L'analyse de timeline permet de reconstituer la chronologie des événements sur un système, essentielle pour comprendre la séquence d'une intrusion.

#### Concepts fondamentaux

**Types de timestamps**
- **MAC Times** : Modified, Accessed, Created
- **Birth Time** : Création du fichier (NTFS)
- **Event Times** : Timestamps des événements système

**Sources de données temporelles**
- Filesystem metadata
- Event logs
- Registry entries
- Browser history
- Network logs
- Application logs

### Création de timelines

#### Outils de création

**Plaso (log2timeline)**
```bash
# Installation
pip install plaso

# Création d'une timeline
log2timeline.py --storage-file timeline.plaso disk_image.dd

# Conversion en CSV
psort.py -o dynamic -w timeline.csv timeline.plaso

# Filtrage temporel
psort.py -o dynamic -w filtered_timeline.csv timeline.plaso "date > '2024-01-01' and date < '2024-01-31'"
```

**Configuration Plaso**
```yaml
# plaso.conf
parsers:
  - chrome_cache
  - chrome_cookies
  - chrome_history
  - firefox_cache
  - firefox_cookies
  - firefox_history
  - windows_registry
  - windows_eventlog
  - prefetch
  - lnk
  - recycle_bin
  - mft
  - usnjrnl

output_format: l2tcsv
timezone: UTC
```

#### Timeline avec TSK

**Création avec fls et mactime**
```bash
# Créer le bodyfile
fls -r -m / disk_image.dd > bodyfile.txt

# Générer la timeline
mactime -b bodyfile.txt -d > filesystem_timeline.csv

# Timeline avec timezone
mactime -b bodyfile.txt -d -z EST5EDT > timeline_est.csv
```

**Timeline avancée**
```bash
# Combiner plusieurs sources
fls -r -m / disk_image.dd > fs_bodyfile.txt
mmls disk_image.dd | grep -E "0[0-9]:" | awk '{print $3}' > partitions.txt

# Créer timeline pour chaque partition
for partition in $(cat partitions.txt); do
    fls -r -m / -o $partition disk_image.dd >> combined_bodyfile.txt
done

mactime -b combined_bodyfile.txt -d > complete_timeline.csv
```

### Corrélation d'événements

#### Corrélation multi-sources

**Script de corrélation**
```python
import pandas as pd
from datetime import datetime, timedelta

def correlate_events(timeline_files, time_window=300):
    """
    Corréler les événements de plusieurs timelines
    time_window: fenêtre de corrélation en secondes
    """
    
    # Charger les timelines
    timelines = {}
    for name, file_path in timeline_files.items():
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        timelines[name] = df
    
    correlations = []
    
    # Comparer chaque événement avec les autres sources
    for source1_name, source1_df in timelines.items():
        for _, event1 in source1_df.iterrows():
            event1_time = event1['timestamp']
            
            for source2_name, source2_df in timelines.items():
                if source1_name != source2_name:
                    # Trouver les événements dans la fenêtre temporelle
                    time_start = event1_time - timedelta(seconds=time_window)
                    time_end = event1_time + timedelta(seconds=time_window)
                    
                    correlated = source2_df[
                        (source2_df['timestamp'] >= time_start) & 
                        (source2_df['timestamp'] <= time_end)
                    ]
                    
                    if not correlated.empty:
                        for _, event2 in correlated.iterrows():
                            correlations.append({
                                'source1': source1_name,
                                'event1': event1,
                                'source2': source2_name,
                                'event2': event2,
                                'time_diff': (event2['timestamp'] - event1_time).total_seconds()
                            })
    
    return correlations

# Utilisation
timeline_files = {
    'filesystem': 'filesystem_timeline.csv',
    'eventlog': 'eventlog_timeline.csv',
    'registry': 'registry_timeline.csv',
    'browser': 'browser_timeline.csv'
}

correlations = correlate_events(timeline_files)
```

#### Détection d'anomalies temporelles

**Analyse des gaps temporels**
```python
def detect_temporal_anomalies(timeline_df, threshold_minutes=60):
    """
    Détecter les anomalies temporelles dans une timeline
    """
    timeline_df['timestamp'] = pd.to_datetime(timeline_df['timestamp'])
    timeline_df = timeline_df.sort_values('timestamp')
    
    # Calculer les intervalles entre événements
    timeline_df['time_diff'] = timeline_df['timestamp'].diff()
    
    # Identifier les gaps importants
    large_gaps = timeline_df[
        timeline_df['time_diff'] > timedelta(minutes=threshold_minutes)
    ]
    
    # Identifier les pics d'activité
    activity_by_minute = timeline_df.groupby(
        timeline_df['timestamp'].dt.floor('1min')
    ).size()
    
    mean_activity = activity_by_minute.mean()
    std_activity = activity_by_minute.std()
    
    activity_spikes = activity_by_minute[
        activity_by_minute > mean_activity + 2 * std_activity
    ]
    
    return {
        'large_gaps': large_gaps,
        'activity_spikes': activity_spikes,
        'stats': {
            'mean_activity_per_minute': mean_activity,
            'std_activity_per_minute': std_activity
        }
    }
```

### Visualisation des données

#### Graphiques temporels

**Visualisation avec matplotlib**
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def create_timeline_visualization(timeline_df, output_path):
    """
    Créer une visualisation de timeline
    """
    timeline_df['timestamp'] = pd.to_datetime(timeline_df['timestamp'])
    
    # Grouper par heure
    hourly_activity = timeline_df.groupby(
        timeline_df['timestamp'].dt.floor('1h')
    ).size()
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(15, 8))
    
    ax.plot(hourly_activity.index, hourly_activity.values, 
            marker='o', linewidth=2, markersize=4)
    
    # Formater les axes
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
    plt.xticks(rotation=45)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Events')
    ax.set_title('Timeline Activity')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

**Visualisation interactive avec Plotly**
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_interactive_timeline(timeline_data, output_path):
    """
    Créer une timeline interactive
    """
    fig = make_subplots(
        rows=len(timeline_data),
        cols=1,
        subplot_titles=list(timeline_data.keys()),
        shared_xaxes=True,
        vertical_spacing=0.02
    )
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, (source, df) in enumerate(timeline_data.items()):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Grouper par heure
        hourly_data = df.groupby(df['timestamp'].dt.floor('1h')).size()
        
        fig.add_trace(
            go.Scatter(
                x=hourly_data.index,
                y=hourly_data.values,
                mode='lines+markers',
                name=source,
                line=dict(color=colors[i % len(colors)]),
                hovertemplate='%{x}<br>Events: %{y}<extra></extra>'
            ),
            row=i+1,
            col=1
        )
    
    fig.update_layout(
        title='Multi-Source Timeline Analysis',
        height=200 * len(timeline_data),
        hovermode='x unified'
    )
    
    fig.write_html(output_path)
```

#### Heatmaps temporelles

**Heatmap d'activité**
```python
import seaborn as sns

def create_activity_heatmap(timeline_df, output_path):
    """
    Créer une heatmap d'activité temporelle
    """
    timeline_df['timestamp'] = pd.to_datetime(timeline_df['timestamp'])
    
    # Extraire les composants temporels
    timeline_df['hour'] = timeline_df['timestamp'].dt.hour
    timeline_df['day'] = timeline_df['timestamp'].dt.day_name()
    
    # Créer la matrice d'activité
    activity_matrix = timeline_df.groupby(['day', 'hour']).size().unstack(fill_value=0)
    
    # Ordonner les jours
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    activity_matrix = activity_matrix.reindex(day_order)
    
    # Créer la heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(activity_matrix, 
                cmap='YlOrRd',
                annot=True,
                fmt='d',
                cbar_kws={'label': 'Number of Events'})
    
    plt.title('Activity Heatmap by Day and Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

Cette approche méthodique des outils et techniques forensiques permet une analyse complète et efficace des systèmes Windows.