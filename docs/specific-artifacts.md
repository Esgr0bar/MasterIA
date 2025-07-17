# Artefacts Spécifiques Windows pour DFIR

## Windows Event Tracing (ETW) - Traces avancées

### Vue d'ensemble d'ETW

Windows Event Tracing (ETW) est un mécanisme de trace haute performance intégré à Windows qui permet de capturer et d'analyser les événements système et d'applications en temps réel.

#### Architecture ETW

**Composants principaux**
- **Providers** : Générateurs d'événements
- **Controllers** : Gestionnaires de sessions de trace
- **Consumers** : Consommateurs d'événements

**Types de providers**
- **Manifest-based** : Définis par des fichiers manifestes
- **MOF-based** : Ancienne méthode (deprecated)
- **TraceLogging** : API moderne pour développeurs

### Configuration d'ETW

#### Outils de configuration

**WPA (Windows Performance Analyzer)**
```cmd
# Lancement de WPA
wpa.exe

# Ouverture d'un fichier ETL
wpa.exe -i trace.etl
```

**WPR (Windows Performance Recorder)**
```cmd
# Profils disponibles
wpr -profiles

# Démarrage d'une trace
wpr -start CPU -start DiskIO

# Arrêt et sauvegarde
wpr -stop trace.etl
```

**Logman**
```cmd
# Créer une session de trace
logman create trace MyTrace -p Microsoft-Windows-Kernel-Process -o trace.etl

# Démarrer la trace
logman start MyTrace

# Arrêter la trace
logman stop MyTrace

# Supprimer la session
logman delete MyTrace
```

#### Configuration avancée

**Profils WPR personnalisés**
```xml
<?xml version="1.0" encoding="utf-8"?>
<WindowsPerformanceRecorder Version="1.0">
  <Profiles>
    <SystemCollector Id="SystemCollector_Custom" Name="Custom System Collector">
      <BufferSize Value="1024"/>
      <Buffers Value="80"/>
    </SystemCollector>
    
    <EventCollector Id="EventCollector_Custom" Name="Custom Event Collector">
      <BufferSize Value="1024"/>
      <Buffers Value="80"/>
    </EventCollector>
    
    <SystemProvider Id="SystemProvider_Custom">
      <Keywords>
        <Keyword Value="ProcessThread"/>
        <Keyword Value="DiskIO"/>
        <Keyword Value="NetworkTrace"/>
      </Keywords>
    </SystemProvider>
    
    <EventProvider Id="Microsoft-Windows-Kernel-Process" Name="Microsoft-Windows-Kernel-Process">
      <Keywords>
        <Keyword Value="0x10"/>
      </Keywords>
    </EventProvider>
    
    <Profile Id="Custom.Verbose.File" Name="Custom" Description="Custom profiling" LoggingMode="File" DetailLevel="Verbose">
      <Collectors>
        <SystemCollectorId Value="SystemCollector_Custom">
          <SystemProviderId Value="SystemProvider_Custom"/>
        </SystemCollectorId>
        <EventCollectorId Value="EventCollector_Custom">
          <EventProviderId Value="Microsoft-Windows-Kernel-Process"/>
        </EventCollectorId>
      </Collectors>
    </Profile>
  </Profiles>
</WindowsPerformanceRecorder>
```

### Analyse des traces ETW

#### Parsing des fichiers ETL

**PowerShell avec Get-WinEvent**
```powershell
# Lecture d'un fichier ETL
Get-WinEvent -Path "C:\traces\trace.etl" | Select-Object TimeCreated, Id, LevelDisplayName, Message

# Filtrage par provider
Get-WinEvent -Path "C:\traces\trace.etl" -FilterHashtable @{ProviderName="Microsoft-Windows-Kernel-Process"}

# Filtrage par Event ID
Get-WinEvent -Path "C:\traces\trace.etl" -FilterHashtable @{Id=1} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $processName = ($eventData | Where-Object {$_.Name -eq "ImageFileName"}).'#text'
    $processId = ($eventData | Where-Object {$_.Name -eq "ProcessId"}).'#text'
    $parentId = ($eventData | Where-Object {$_.Name -eq "ParentProcessId"}).'#text'
    
    Write-Host "Process: $processName (PID: $processId, PPID: $parentId)"
}
```

**Python avec python-etw**
```python
import etw

def process_event(event_record):
    """Process ETW event"""
    if event_record.EventHeader.ProviderId == "{22fb2cd6-0e7b-422b-a0c7-2fad1fd0e716}":  # Kernel-Process
        event_data = event_record.EventData
        print(f"Process Event: {event_data}")

# Créer un consumer ETW
consumer = etw.ETWConsumer()
consumer.start_trace("MyTrace")
consumer.register_callback(process_event)
consumer.process_events()
```

#### Analyse des événements spécifiques

**Analyse des processus**
```powershell
# Événements de création de processus (Event ID 1)
Get-WinEvent -Path "trace.etl" -FilterHashtable @{ProviderName="Microsoft-Windows-Kernel-Process"; Id=1} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $processName = ($eventData | Where-Object {$_.Name -eq "ImageFileName"}).'#text'
    $processId = ($eventData | Where-Object {$_.Name -eq "ProcessId"}).'#text'
    $parentId = ($eventData | Where-Object {$_.Name -eq "ParentProcessId"}).'#text'
    $commandLine = ($eventData | Where-Object {$_.Name -eq "CommandLine"}).'#text'
    
    [PSCustomObject]@{
        TimeCreated = $_.TimeCreated
        ProcessName = $processName
        ProcessId = $processId
        ParentProcessId = $parentId
        CommandLine = $commandLine
    }
}
```

**Analyse des accès fichiers**
```powershell
# Événements d'accès fichier
Get-WinEvent -Path "trace.etl" -FilterHashtable @{ProviderName="Microsoft-Windows-Kernel-File"} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $fileName = ($eventData | Where-Object {$_.Name -eq "FileName"}).'#text'
    $processId = ($eventData | Where-Object {$_.Name -eq "ProcessId"}).'#text'
    $operation = ($eventData | Where-Object {$_.Name -eq "Operation"}).'#text'
    
    [PSCustomObject]@{
        TimeCreated = $_.TimeCreated
        FileName = $fileName
        ProcessId = $processId
        Operation = $operation
    }
}
```

### Corrélation avec autres artefacts

#### Corrélation avec Event Logs

**Corrélation ProcessId**
```powershell
# Récupérer les processus depuis ETW
$etwProcesses = Get-WinEvent -Path "trace.etl" -FilterHashtable @{ProviderName="Microsoft-Windows-Kernel-Process"; Id=1}

# Récupérer les événements de sécurité
$securityEvents = Get-WinEvent -LogName "Security" -FilterHashtable @{Id=4688}

# Corréler par ProcessId et timestamp
foreach ($etwProcess in $etwProcesses) {
    $etwEvent = [xml]$etwProcess.ToXml()
    $etwProcessId = ($etwEvent.Event.EventData.Data | Where-Object {$_.Name -eq "ProcessId"}).'#text'
    $etwTime = $etwProcess.TimeCreated
    
    $correlatedEvents = $securityEvents | Where-Object {
        $secEvent = [xml]$_.ToXml()
        $secProcessId = ($secEvent.Event.EventData.Data | Where-Object {$_.Name -eq "NewProcessId"}).'#text'
        $secTime = $_.TimeCreated
        
        return $secProcessId -eq $etwProcessId -and (($secTime - $etwTime).TotalSeconds -lt 5)
    }
    
    if ($correlatedEvents) {
        Write-Host "Correlated process $etwProcessId at $etwTime"
    }
}
```

#### Corrélation avec Sysmon

**Corrélation multi-sources**
```powershell
function Correlate-Events {
    param(
        [string]$ETWFile,
        [datetime]$StartTime,
        [datetime]$EndTime
    )
    
    # ETW Events
    $etwEvents = Get-WinEvent -Path $ETWFile -FilterHashtable @{
        ProviderName="Microsoft-Windows-Kernel-Process"
        StartTime=$StartTime
        EndTime=$EndTime
    }
    
    # Sysmon Events
    $sysmonEvents = Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -FilterHashtable @{
        StartTime=$StartTime
        EndTime=$EndTime
    }
    
    # Security Events
    $securityEvents = Get-WinEvent -LogName "Security" -FilterHashtable @{
        StartTime=$StartTime
        EndTime=$EndTime
    }
    
    $correlatedEvents = @()
    
    foreach ($etwEvent in $etwEvents) {
        $etwXml = [xml]$etwEvent.ToXml()
        $etwProcessId = ($etwXml.Event.EventData.Data | Where-Object {$_.Name -eq "ProcessId"}).'#text'
        $etwTime = $etwEvent.TimeCreated
        
        # Trouver les événements Sysmon correspondants
        $matchingSysmon = $sysmonEvents | Where-Object {
            $sysmonXml = [xml]$_.ToXml()
            $sysmonProcessId = ($sysmonXml.Event.EventData.Data | Where-Object {$_.Name -eq "ProcessId"}).'#text'
            $sysmonTime = $_.TimeCreated
            
            return $sysmonProcessId -eq $etwProcessId -and (($sysmonTime - $etwTime).TotalSeconds -lt 2)
        }
        
        if ($matchingSysmon) {
            $correlatedEvents += [PSCustomObject]@{
                ETWEvent = $etwEvent
                SysmonEvents = $matchingSysmon
                ProcessId = $etwProcessId
                TimeCreated = $etwTime
            }
        }
    }
    
    return $correlatedEvents
}
```

### Outils d'analyse ETW

#### WPA (Windows Performance Analyzer)

**Configuration des vues**
```xml
<!-- Custom WPA Profile -->
<WpaProfile>
  <TraceMergeProperties>
    <TraceMergeProperty Id="Microsoft-Windows-Kernel-Process" Name="Process Events"/>
  </TraceMergeProperties>
  
  <Views>
    <View Title="Process Timeline" Type="Timeline">
      <Graphs>
        <Graph Title="Process Creation" Type="Line">
          <Data>
            <Series Name="ProcessId" Type="Numeric"/>
            <Series Name="ProcessName" Type="String"/>
          </Data>
        </Graph>
      </Graphs>
    </View>
  </Views>
</WpaProfile>
```

#### Krabsetw

**Utilisation de Krabsetw (C++)**
```cpp
#include <krabs.hpp>

void analyze_etw_trace(const std::string& etl_file) {
    krabs::etl_file_reader reader(etl_file);
    
    // Provider pour processus
    krabs::provider<> kernel_process_provider(L"Microsoft-Windows-Kernel-Process");
    
    // Callback pour événements de processus
    kernel_process_provider.on_event([](const krabs::event_record& record) {
        krabs::schema schema(record);
        
        if (schema.event_id() == 1) {  // Process creation
            auto process_id = schema.process_id();
            auto image_name = schema.get_unicode_string(L"ImageFileName");
            auto command_line = schema.get_unicode_string(L"CommandLine");
            
            std::wcout << L"Process created: " << image_name 
                      << L" (PID: " << process_id 
                      << L", CMD: " << command_line << L")" << std::endl;
        }
    });
    
    reader.add_provider(kernel_process_provider);
    reader.start();
}
```

## Windows Performance Toolkit - Analyse des performances

### Vue d'ensemble de WPT

Le Windows Performance Toolkit (WPT) est une collection d'outils de Microsoft pour l'analyse des performances système, utile en forensique pour comprendre les comportements système.

#### Composants principaux

**WPR (Windows Performance Recorder)**
- Capture de traces système
- Profils prédéfinis
- Configuration personnalisée

**WPA (Windows Performance Analyzer)**
- Analyse des traces
- Visualisation des données
- Corrélation d'événements

**Xperf (ligne de commande)**
- Interface legacy
- Scripting avancé
- Automatisation

### Utilisation de WPT pour la forensique

#### Capture d'événements système

**Profil de capture généraliste**
```cmd
# Démarrer la capture
wpr -start GeneralProfile -start CPU -start DiskIO -start Registry

# Activité suspecte...

# Arrêter et sauvegarder
wpr -stop forensic_trace.etl
```

**Profil personnalisé pour forensique**
```xml
<?xml version="1.0" encoding="utf-8"?>
<WindowsPerformanceRecorder Version="1.0">
  <Profiles>
    <SystemCollector Id="ForensicSystemCollector" Name="Forensic System Collector">
      <BufferSize Value="1024"/>
      <Buffers Value="128"/>
    </SystemCollector>
    
    <EventCollector Id="ForensicEventCollector" Name="Forensic Event Collector">
      <BufferSize Value="1024"/>
      <Buffers Value="128"/>
    </EventCollector>
    
    <SystemProvider Id="ForensicSystemProvider">
      <Keywords>
        <Keyword Value="ProcessThread"/>
        <Keyword Value="Loader"/>
        <Keyword Value="DiskIO"/>
        <Keyword Value="HardFaults"/>
        <Keyword Value="VirtualAlloc"/>
        <Keyword Value="NetworkTrace"/>
        <Keyword Value="Registry"/>
      </Keywords>
    </SystemProvider>
    
    <EventProvider Id="Microsoft-Windows-Kernel-Process" Name="Microsoft-Windows-Kernel-Process">
      <Keywords>
        <Keyword Value="0xFFFFFFFFFFFFFFF"/>
      </Keywords>
    </EventProvider>
    
    <EventProvider Id="Microsoft-Windows-Security-Auditing" Name="Microsoft-Windows-Security-Auditing">
      <Keywords>
        <Keyword Value="0xFFFFFFFFFFFFFFF"/>
      </Keywords>
    </EventProvider>
    
    <Profile Id="Forensic.Verbose.File" Name="Forensic" Description="Forensic investigation profile" LoggingMode="File" DetailLevel="Verbose">
      <Collectors>
        <SystemCollectorId Value="ForensicSystemCollector">
          <SystemProviderId Value="ForensicSystemProvider"/>
        </SystemCollectorId>
        <EventCollectorId Value="ForensicEventCollector">
          <EventProviderId Value="Microsoft-Windows-Kernel-Process"/>
          <EventProviderId Value="Microsoft-Windows-Security-Auditing"/>
        </EventCollectorId>
      </Collectors>
    </Profile>
  </Profiles>
</WindowsPerformanceRecorder>
```

#### Analyse des traces de performance

**Analyse des processus**
```powershell
# Extraire les données de processus depuis WPA
function Extract-ProcessData {
    param([string]$ETLFile)
    
    # Utiliser WPA en mode ligne de commande
    $wpaScript = @"
    import sys
    from wpa import *
    
    # Ouvrir la trace
    trace = Analysis()
    trace.open('$ETLFile')
    
    # Extraire les données de processus
    process_table = trace.get_table('Processes')
    
    for row in process_table:
        print(f"Process: {row.Process}, PID: {row.ProcessId}, Start: {row.CreateTime}")
"@
    
    # Sauvegarder le script
    $wpaScript | Out-File -FilePath "extract_processes.py"
    
    # Exécuter avec WPA
    wpa.exe -i $ETLFile -script extract_processes.py
}
```

**Analyse des I/O disque**
```powershell
function Analyze-DiskIO {
    param([string]$ETLFile)
    
    # Script WPA pour analyser les I/O
    $ioScript = @"
    trace = Analysis()
    trace.open('$ETLFile')
    
    # Table des I/O disque
    disk_table = trace.get_table('Disk Usage')
    
    suspicious_io = []
    
    for row in disk_table:
        if row.Size > 10485760:  # 10MB
            suspicious_io.append({
                'Process': row.Process,
                'File': row.FileName,
                'Size': row.Size,
                'Time': row.Timestamp
            })
    
    for io in suspicious_io:
        print(f"Large I/O: {io['Process']} -> {io['File']} ({io['Size']} bytes)")
"@
    
    $ioScript | Out-File -FilePath "analyze_disk_io.py"
    wpa.exe -i $ETLFile -script analyze_disk_io.py
}
```

### Corrélation avec les incidents

#### Timeline des événements

**Création de timeline**
```powershell
function Create-IncidentTimeline {
    param(
        [string]$ETLFile,
        [datetime]$IncidentTime,
        [int]$WindowMinutes = 30
    )
    
    $startTime = $IncidentTime.AddMinutes(-$WindowMinutes)
    $endTime = $IncidentTime.AddMinutes($WindowMinutes)
    
    # Événements ETW
    $etwEvents = Get-WinEvent -Path $ETLFile -FilterHashtable @{
        StartTime = $startTime
        EndTime = $endTime
    }
    
    # Événements système
    $systemEvents = Get-WinEvent -LogName "System" -FilterHashtable @{
        StartTime = $startTime
        EndTime = $endTime
    }
    
    # Événements de sécurité
    $securityEvents = Get-WinEvent -LogName "Security" -FilterHashtable @{
        StartTime = $startTime
        EndTime = $endTime
    }
    
    # Combiner et trier
    $allEvents = @()
    $allEvents += $etwEvents | ForEach-Object { @{Source="ETW"; Event=$_} }
    $allEvents += $systemEvents | ForEach-Object { @{Source="System"; Event=$_} }
    $allEvents += $securityEvents | ForEach-Object { @{Source="Security"; Event=$_} }
    
    $timeline = $allEvents | Sort-Object {$_.Event.TimeCreated}
    
    # Exporter la timeline
    $timeline | ForEach-Object {
        [PSCustomObject]@{
            TimeCreated = $_.Event.TimeCreated
            Source = $_.Source
            Id = $_.Event.Id
            Level = $_.Event.LevelDisplayName
            Message = $_.Event.Message
        }
    } | Export-Csv -Path "incident_timeline.csv" -NoTypeInformation
}
```

#### Analyse des anomalies

**Détection d'anomalies de performance**
```powershell
function Detect-PerformanceAnomalies {
    param([string]$ETLFile)
    
    # Analyser les métriques de performance
    $performanceScript = @"
    trace = Analysis()
    trace.open('$ETLFile')
    
    # CPU Usage
    cpu_table = trace.get_table('CPU Usage (Sampled)')
    cpu_usage = {}
    
    for row in cpu_table:
        process = row.Process
        if process not in cpu_usage:
            cpu_usage[process] = 0
        cpu_usage[process] += row.Weight
    
    # Détecter les processus avec utilisation CPU élevée
    for process, usage in cpu_usage.items():
        if usage > 80:  # Plus de 80% CPU
            print(f"High CPU usage: {process} - {usage}%")
    
    # Memory Usage
    memory_table = trace.get_table('Virtual Memory Snapshots')
    memory_usage = {}
    
    for row in memory_table:
        process = row.Process
        if process not in memory_usage:
            memory_usage[process] = 0
        memory_usage[process] += row.Size
    
    # Détecter les processus avec utilisation mémoire élevée
    for process, usage in memory_usage.items():
        if usage > 1073741824:  # Plus de 1GB
            print(f"High memory usage: {process} - {usage/1073741824:.2f}GB")
"@
    
    $performanceScript | Out-File -FilePath "detect_anomalies.py"
    wpa.exe -i $ETLFile -script detect_anomalies.py
}
```

### Optimisation des analyses

#### Filtrage des données

**Filtres WPA**
```xml
<!-- Filtre pour processus spécifiques -->
<Filter Name="SuspiciousProcesses">
  <Column Name="Process">
    <Value>powershell.exe</Value>
    <Value>cmd.exe</Value>
    <Value>rundll32.exe</Value>
    <Value>regsvr32.exe</Value>
  </Column>
</Filter>

<!-- Filtre temporel -->
<Filter Name="IncidentTimeframe">
  <Column Name="TimeStamp">
    <Range Start="2024-01-15T14:00:00" End="2024-01-15T16:00:00"/>
  </Column>
</Filter>
```

## PowerShell Forensics - Analyse des scripts

### Vue d'ensemble de PowerShell Forensics

PowerShell étant largement utilisé par les attaquants, son analyse forensique est cruciale pour comprendre les activités malveillantes.

#### Sources d'artefacts PowerShell

**Logs PowerShell**
- Microsoft-Windows-PowerShell/Operational
- Microsoft-Windows-PowerShell/Analytic
- Windows PowerShell.evtx

**Fichiers de configuration**
- Profile.ps1
- Modules personnalisés
- Historique des commandes

**Artefacts mémoire**
- Processus PowerShell
- Modules chargés
- Variables d'environnement

### Logs PowerShell

#### Configuration du logging

**Activation du logging avancé**
```powershell
# Via Group Policy ou Registry
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging" -Name "EnableModuleLogging" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -Name "EnableScriptBlockLogging" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription" -Name "EnableTranscripting" -Value 1
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription" -Name "OutputDirectory" -Value "C:\PSTranscripts"
```

**Configuration via GPO**
```xml
<!-- PowerShell Logging GPO -->
<policy>
  <name>Turn on PowerShell Script Block Logging</name>
  <state>Enabled</state>
  <registry>
    <path>HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging</path>
    <value name="EnableScriptBlockLogging" type="REG_DWORD" data="1"/>
  </registry>
</policy>
```

#### Analyse des logs

**Event ID 4104 - Script Block Logging**
```powershell
# Analyser les script blocks
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-PowerShell/Operational"; ID=4104} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $scriptBlock = ($eventData | Where-Object {$_.Name -eq "ScriptBlockText"}).'#text'
    $scriptBlockId = ($eventData | Where-Object {$_.Name -eq "ScriptBlockId"}).'#text'
    $path = ($eventData | Where-Object {$_.Name -eq "Path"}).'#text'
    
    [PSCustomObject]@{
        TimeCreated = $_.TimeCreated
        ScriptBlockId = $scriptBlockId
        Path = $path
        ScriptBlock = $scriptBlock
    }
} | Where-Object {$_.ScriptBlock -match "invoke-|download|iex|iwr|empire|mimikatz"}
```

**Event ID 4103 - Module Logging**
```powershell
# Analyser les modules chargés
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-PowerShell/Operational"; ID=4103} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $commandName = ($eventData | Where-Object {$_.Name -eq "CommandName"}).'#text'
    $commandType = ($eventData | Where-Object {$_.Name -eq "CommandType"}).'#text'
    $hostName = ($eventData | Where-Object {$_.Name -eq "HostName"}).'#text'
    $commandLine = ($eventData | Where-Object {$_.Name -eq "CommandLine"}).'#text'
    
    [PSCustomObject]@{
        TimeCreated = $_.TimeCreated
        CommandName = $commandName
        CommandType = $commandType
        HostName = $hostName
        CommandLine = $commandLine
    }
}
```

### Analyse des scripts malveillants

#### Détection de patterns malveillants

**Indicateurs communs**
```powershell
function Detect-MaliciousPatterns {
    param([string]$ScriptContent)
    
    $maliciousPatterns = @(
        "Invoke-Expression",
        "IEX",
        "Invoke-WebRequest",
        "IWR",
        "DownloadString",
        "DownloadFile",
        "System.Net.WebClient",
        "New-Object Net.WebClient",
        "Start-Process",
        "cmd.exe /c",
        "powershell.exe -e",
        "powershell.exe -en",
        "powershell.exe -enc",
        "FromBase64String",
        "Convert.*Base64",
        "Reflection.Assembly",
        "System.Reflection.Assembly",
        "Load.*Assembly",
        "Invoke-Mimikatz",
        "Invoke-Kerberoast",
        "Invoke-BloodHound",
        "Empire",
        "Metasploit",
        "Meterpreter",
        "Add-Type",
        "DllImport",
        "VirtualAlloc",
        "CreateThread",
        "WaitForSingleObject",
        "kernel32",
        "ntdll",
        "Get-Process.*Stop-Process",
        "Get-Service.*Stop-Service",
        "Remove-Item.*-Recurse",
        "Clear-EventLog",
        "wevtutil.*cl",
        "Get-EventLog.*Clear-EventLog"
    )
    
    $detectedPatterns = @()
    
    foreach ($pattern in $maliciousPatterns) {
        if ($ScriptContent -match $pattern) {
            $detectedPatterns += $pattern
        }
    }
    
    return $detectedPatterns
}

# Exemple d'utilisation
$scriptContent = Get-Content "suspicious_script.ps1" -Raw
$patterns = Detect-MaliciousPatterns -ScriptContent $scriptContent
if ($patterns) {
    Write-Host "Malicious patterns detected: $($patterns -join ', ')"
}
```

#### Déobfuscation de scripts

**Déobfuscation basique**
```powershell
function Deobfuscate-PowerShellScript {
    param([string]$ObfuscatedScript)
    
    # Remplacer les variables communes
    $deobfuscated = $ObfuscatedScript
    $deobfuscated = $deobfuscated -replace '\$env:.*?\+', ''
    $deobfuscated = $deobfuscated -replace '\${.*?}', 'VAR'
    $deobfuscated = $deobfuscated -replace '\[char\]\d+', 'CHAR'
    
    # Décoder Base64
    $base64Pattern = '[A-Za-z0-9+/]+=*'
    $base64Matches = [regex]::Matches($deobfuscated, $base64Pattern)
    
    foreach ($match in $base64Matches) {
        if ($match.Value.Length -gt 20) {
            try {
                $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($match.Value))
                $deobfuscated = $deobfuscated.Replace($match.Value, $decoded)
            } catch {
                # Ignore invalid base64
            }
        }
    }
    
    # Remplacer les concaténations
    $deobfuscated = $deobfuscated -replace '\+\s*', ''
    $deobfuscated = $deobfuscated -replace "''\s*\+\s*''"
    
    return $deobfuscated
}
```

### Techniques d'évasion PowerShell

#### Obfuscation courante

**Invoke-Obfuscation**
```powershell
# Exemples d'obfuscation détectés
$obfuscatedExamples = @(
    # Concatenation
    "('In'+'voke-Ex'+'pression')",
    
    # Character codes
    "[char]73+[char]110+[char]118+[char]111+[char]107+[char]101",
    
    # Variable substitution
    '$a='+"'"+'Invoke-Expression'+"'"+';IEX $a',
    
    # Format strings
    "'{0}{1}{2}' -f 'Inv','oke-Ex','pression'",
    
    # Reverse strings
    "'noisserpxE-ekovnI'[-1..-16] -join ''",
    
    # Base64 encoding
    "([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('SW52b2tlLUV4cHJlc3Npb24=')))"
)
```

#### Détection d'évasion

**Analyse des techniques d'évasion**
```powershell
function Detect-EvasionTechniques {
    param([string]$ScriptContent)
    
    $evasionTechniques = @()
    
    # Détection de base64
    if ($ScriptContent -match 'FromBase64String|Convert.*Base64') {
        $evasionTechniques += "Base64 Encoding"
    }
    
    # Détection de concaténation
    if ($ScriptContent -match "'\+'|''\s*\+\s*''") {
        $evasionTechniques += "String Concatenation"
    }
    
    # Détection de format strings
    if ($ScriptContent -match '-f\s+') {
        $evasionTechniques += "Format String"
    }
    
    # Détection de caractères ASCII
    if ($ScriptContent -match '\[char\]\d+') {
        $evasionTechniques += "ASCII Character Codes"
    }
    
    # Détection de variables
    if ($ScriptContent -match '\$\w+\s*=\s*[''"].*[''"]') {
        $evasionTechniques += "Variable Substitution"
    }
    
    # Détection de compression
    if ($ScriptContent -match 'IO\.Compression|GZipStream') {
        $evasionTechniques += "Compression"
    }
    
    # Détection de split/join
    if ($ScriptContent -match 'split|join') {
        $evasionTechniques += "Split/Join Operations"
    }
    
    return $evasionTechniques
}
```

### Outils d'analyse PowerShell

#### PowerShell Empire Detection

**Détection d'Empire**
```powershell
function Detect-PowerShellEmpire {
    param([string]$LogPath)
    
    $empireIndicators = @(
        "Microsoft.PowerShell.Commands.InvokeExpressionCommand",
        "System.Management.Automation.AmsiUtils",
        "Invoke-Empire",
        "powershell.exe.*-W Hidden.*-nop",
        "powershell.exe.*-windowstyle hidden",
        "Empire",
        "stage0",
        "stage1",
        "stage2",
        "checkin",
        "tasking",
        "JobTracking",
        "StagingKey",
        "SessionKey"
    )
    
    $empireEvents = Get-WinEvent -Path $LogPath -FilterHashtable @{LogName="Microsoft-Windows-PowerShell/Operational"} | Where-Object {
        $message = $_.Message
        $empireIndicators | Where-Object { $message -match $_ }
    }
    
    return $empireEvents
}
```

#### Revoke-Obfuscation

**Utilisation de Revoke-Obfuscation**
```powershell
Import-Module Revoke-Obfuscation

# Analyser un script obfusqué
$scriptContent = Get-Content "obfuscated_script.ps1" -Raw
$results = Measure-RvoObfuscation -ScriptBlock $scriptContent

# Afficher les résultats
$results | Format-Table -AutoSize
```

Cette approche complète permet d'analyser efficacement les artefacts ETW, les performances système et les activités PowerShell dans un contexte forensique.