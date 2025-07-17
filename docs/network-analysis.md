# Analyse Réseau pour la Forensique Windows

## Network Forensics sur Windows - Analyse des communications

### Vue d'ensemble de l'analyse réseau

L'analyse réseau forensique consiste à capturer, analyser et interpréter le trafic réseau pour identifier des activités malveillantes, reconstituer des événements et collecter des preuves.

#### Objectifs de l'analyse réseau

**Détection d'intrusion**
- Identification des connexions non autorisées
- Détection d'exfiltration de données
- Analyse des communications de malwares

**Reconstruction d'événements**
- Chronologie des communications
- Identification des acteurs
- Mapping des infrastructures malveillantes

**Collecte de preuves**
- Capture des communications
- Extraction d'artefacts réseau
- Documentation des activités

### Capture de trafic réseau

#### Outils de capture

**Wireshark**
```bash
# Capture sur interface spécifique
wireshark -i eth0 -w capture.pcap

# Capture avec filtre
wireshark -i eth0 -f "host 192.168.1.100" -w targeted_capture.pcap

# Capture en ligne de commande
tshark -i eth0 -w network_traffic.pcap
```

**tcpdump**
```bash
# Capture basique
tcpdump -i eth0 -w network.pcap

# Capture avec filtres
tcpdump -i eth0 host 192.168.1.100 and port 80 -w http_traffic.pcap

# Capture DNS
tcpdump -i eth0 port 53 -w dns_traffic.pcap

# Capture avec timestamp
tcpdump -i eth0 -tttt -w timestamped.pcap
```

**netsh (Windows)**
```cmd
# Démarrer la capture
netsh trace start capture=yes tracefile=network.etl provider=Microsoft-Windows-TCPIP

# Arrêter la capture
netsh trace stop

# Conversion en pcap
netsh trace convert network.etl output=network.pcap
```

#### Configuration avancée

**Mirrors de ports**
```bash
# Configuration switch Cisco
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 100

monitor session 1 source interface GigabitEthernet0/1
monitor session 1 destination interface GigabitEthernet0/24
```

**TAP réseau**
```bash
# Configuration avec ntopng
ntopng -i eth0 -P /var/lib/ntopng/ntopng.pid -d /var/lib/ntopng -w 3000
```

### Analyse des connexions TCP/UDP

#### Analyse des flux TCP

**Reconstruction des sessions**
```python
import pyshark

def analyze_tcp_streams(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    tcp_streams = {}
    
    for packet in cap:
        if hasattr(packet, 'tcp'):
            stream_id = packet.tcp.stream
            
            if stream_id not in tcp_streams:
                tcp_streams[stream_id] = {
                    'packets': [],
                    'src_ip': packet.ip.src,
                    'dst_ip': packet.ip.dst,
                    'src_port': packet.tcp.srcport,
                    'dst_port': packet.tcp.dstport,
                    'start_time': packet.sniff_time,
                    'bytes_sent': 0,
                    'bytes_received': 0
                }
            
            tcp_streams[stream_id]['packets'].append(packet)
            
            # Calculer les statistiques
            if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'len'):
                tcp_streams[stream_id]['bytes_sent'] += int(packet.tcp.len)
    
    return tcp_streams
```

**Détection d'anomalies TCP**
```python
def detect_tcp_anomalies(tcp_streams):
    anomalies = []
    
    for stream_id, stream in tcp_streams.items():
        # Connexions sur ports non standard
        if int(stream['dst_port']) not in [80, 443, 22, 21, 25, 110, 143]:
            anomalies.append(f"Stream {stream_id}: Non-standard port {stream['dst_port']}")
        
        # Ratio de données suspect
        if stream['bytes_sent'] > 10000000:  # 10MB
            anomalies.append(f"Stream {stream_id}: Large data transfer")
        
        # Connexions longues
        duration = (stream['packets'][-1].sniff_time - stream['start_time']).total_seconds()
        if duration > 3600:  # 1 heure
            anomalies.append(f"Stream {stream_id}: Long connection ({duration}s)")
    
    return anomalies
```

#### Analyse UDP

**Analyse des flux UDP**
```python
def analyze_udp_traffic(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    udp_flows = {}
    
    for packet in cap:
        if hasattr(packet, 'udp'):
            flow_key = f"{packet.ip.src}:{packet.udp.srcport}->{packet.ip.dst}:{packet.udp.dstport}"
            
            if flow_key not in udp_flows:
                udp_flows[flow_key] = {
                    'packets': [],
                    'total_bytes': 0,
                    'start_time': packet.sniff_time,
                    'last_time': packet.sniff_time
                }
            
            udp_flows[flow_key]['packets'].append(packet)
            udp_flows[flow_key]['total_bytes'] += int(packet.udp.length)
            udp_flows[flow_key]['last_time'] = packet.sniff_time
    
    return udp_flows
```

**Détection de tunneling DNS**
```python
def detect_dns_tunneling(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    dns_queries = {}
    
    for packet in cap:
        if hasattr(packet, 'dns') and packet.dns.flags_response == '0':
            query_name = packet.dns.qry_name
            
            if query_name not in dns_queries:
                dns_queries[query_name] = []
            
            dns_queries[query_name].append(packet)
    
    # Détection de tunneling
    suspicious_domains = []
    for domain, queries in dns_queries.items():
        if len(queries) > 100:  # Nombreuses requêtes
            suspicious_domains.append(domain)
        
        # Sous-domaines longs (potentiel tunneling)
        if len(domain.split('.')[0]) > 50:
            suspicious_domains.append(domain)
    
    return suspicious_domains
```

### Logs réseau Windows

#### Event Logs réseau

**Security Event Log**
```powershell
# Événements de connexion réseau
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=5156} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $data = $event.Event.EventData.Data
    
    Write-Host "Source IP: $($data[0].'#text')"
    Write-Host "Source Port: $($data[1].'#text')"
    Write-Host "Destination IP: $($data[2].'#text')"
    Write-Host "Destination Port: $($data[3].'#text')"
    Write-Host "Protocol: $($data[4].'#text')"
    Write-Host "---"
}
```

**Firewall Logs**
```powershell
# Activation du logging firewall
netsh advfirewall set allprofiles logging filename %systemroot%\system32\LogFiles\Firewall\pfirewall.log
netsh advfirewall set allprofiles logging maxfilesize 4096
netsh advfirewall set allprofiles logging droppedconnections enable
netsh advfirewall set allprofiles logging allowedconnections enable

# Analyse des logs
Get-Content C:\Windows\system32\LogFiles\Firewall\pfirewall.log | Where-Object {$_ -like "*DROP*"} | Select-Object -First 10
```

#### Sysmon Network Events

**Configuration Sysmon**
```xml
<Sysmon schemaversion="4.30">
  <EventFiltering>
    <NetworkConnect onmatch="include">
      <Image condition="end with">cmd.exe</Image>
      <Image condition="end with">powershell.exe</Image>
      <Image condition="end with">rundll32.exe</Image>
    </NetworkConnect>
  </EventFiltering>
</Sysmon>
```

**Analyse des événements Sysmon**
```powershell
# Connexions réseau (Event ID 3)
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-Sysmon/Operational"; ID=3} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $processName = ($eventData | Where-Object {$_.Name -eq "Image"}).'#text'
    $destIP = ($eventData | Where-Object {$_.Name -eq "DestinationIp"}).'#text'
    $destPort = ($eventData | Where-Object {$_.Name -eq "DestinationPort"}).'#text'
    
    Write-Host "Process: $processName -> $destIP:$destPort"
}
```

### Détection d'activités malveillantes

#### Indicateurs de compromission réseau

**Beaconing**
```python
def detect_beaconing(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    connections = {}
    
    for packet in cap:
        if hasattr(packet, 'ip') and hasattr(packet, 'tcp'):
            key = f"{packet.ip.src}->{packet.ip.dst}:{packet.tcp.dstport}"
            
            if key not in connections:
                connections[key] = []
            
            connections[key].append(packet.sniff_time)
    
    # Analyser les intervalles
    beacons = []
    for conn, timestamps in connections.items():
        if len(timestamps) > 10:
            intervals = []
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervals.append(interval)
            
            # Vérifier la régularité
            if len(intervals) > 5:
                avg_interval = sum(intervals) / len(intervals)
                variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
                
                if variance < 10:  # Faible variance = beaconing
                    beacons.append({
                        'connection': conn,
                        'interval': avg_interval,
                        'variance': variance,
                        'count': len(timestamps)
                    })
    
    return beacons
```

**Exfiltration de données**
```python
def detect_data_exfiltration(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    external_transfers = {}
    
    for packet in cap:
        if hasattr(packet, 'ip') and hasattr(packet, 'tcp'):
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            
            # Vérifier si destination externe
            if not dst_ip.startswith('192.168.') and not dst_ip.startswith('10.'):
                key = f"{src_ip}->{dst_ip}"
                
                if key not in external_transfers:
                    external_transfers[key] = 0
                
                if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'len'):
                    external_transfers[key] += int(packet.tcp.len)
    
    # Identifier les transferts suspects
    suspicious_transfers = []
    for transfer, bytes_sent in external_transfers.items():
        if bytes_sent > 10000000:  # 10MB
            suspicious_transfers.append({
                'transfer': transfer,
                'bytes': bytes_sent,
                'mb': bytes_sent / (1024 * 1024)
            })
    
    return suspicious_transfers
```

#### Analyse des protocoles

**HTTP Analysis**
```python
def analyze_http_traffic(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    http_requests = []
    
    for packet in cap:
        if hasattr(packet, 'http'):
            if hasattr(packet.http, 'request_method'):
                request = {
                    'timestamp': packet.sniff_time,
                    'src_ip': packet.ip.src,
                    'dst_ip': packet.ip.dst,
                    'method': packet.http.request_method,
                    'host': packet.http.host if hasattr(packet.http, 'host') else 'Unknown',
                    'uri': packet.http.request_uri if hasattr(packet.http, 'request_uri') else 'Unknown',
                    'user_agent': packet.http.user_agent if hasattr(packet.http, 'user_agent') else 'Unknown'
                }
                
                http_requests.append(request)
    
    return http_requests
```

**HTTPS Analysis**
```python
def analyze_tls_traffic(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    tls_sessions = []
    
    for packet in cap:
        if hasattr(packet, 'tls'):
            if hasattr(packet.tls, 'handshake_extensions_server_name'):
                session = {
                    'timestamp': packet.sniff_time,
                    'src_ip': packet.ip.src,
                    'dst_ip': packet.ip.dst,
                    'server_name': packet.tls.handshake_extensions_server_name,
                    'cipher_suite': packet.tls.handshake_ciphersuite if hasattr(packet.tls, 'handshake_ciphersuite') else 'Unknown'
                }
                
                tls_sessions.append(session)
    
    return tls_sessions
```

## Analyse des Shares et RPC - Communication inter-processus

### SMB/CIFS forensics

#### Analyse du trafic SMB

**Capture SMB**
```bash
# Capture du trafic SMB
tshark -i eth0 -f "port 445 or port 139" -w smb_traffic.pcap

# Analyse avec Wireshark
wireshark -r smb_traffic.pcap -Y "smb2"
```

**Extraction des fichiers SMB**
```python
import pyshark

def extract_smb_files(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    smb_files = []
    
    for packet in cap:
        if hasattr(packet, 'smb2'):
            if hasattr(packet.smb2, 'filename'):
                file_info = {
                    'timestamp': packet.sniff_time,
                    'src_ip': packet.ip.src,
                    'dst_ip': packet.ip.dst,
                    'filename': packet.smb2.filename,
                    'share': packet.smb2.tree if hasattr(packet.smb2, 'tree') else 'Unknown',
                    'command': packet.smb2.cmd if hasattr(packet.smb2, 'cmd') else 'Unknown'
                }
                
                smb_files.append(file_info)
    
    return smb_files
```

#### Analyse des événements SMB

**Audit SMB**
```powershell
# Activation de l'audit SMB
auditpol /set /subcategory:"File Share" /success:enable /failure:enable
auditpol /set /subcategory:"Detailed File Share" /success:enable /failure:enable

# Analyse des événements
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=5140} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $subject = ($eventData | Where-Object {$_.Name -eq "SubjectUserName"}).'#text'
    $shareName = ($eventData | Where-Object {$_.Name -eq "ShareName"}).'#text'
    $sourceIP = ($eventData | Where-Object {$_.Name -eq "IpAddress"}).'#text'
    
    Write-Host "User: $subject accessed share: $shareName from IP: $sourceIP"
}
```

### RPC et named pipes

#### Analyse RPC

**Capture RPC**
```bash
# Capture du trafic RPC
tshark -i eth0 -f "port 135" -w rpc_traffic.pcap

# Analyse avec Wireshark
wireshark -r rpc_traffic.pcap -Y "dcerpc"
```

**Analyse des named pipes**
```python
def analyze_named_pipes(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    
    named_pipes = []
    
    for packet in cap:
        if hasattr(packet, 'smb2') and hasattr(packet.smb2, 'filename'):
            filename = packet.smb2.filename
            
            if filename.startswith('\\\\'):
                pipe_info = {
                    'timestamp': packet.sniff_time,
                    'src_ip': packet.ip.src,
                    'dst_ip': packet.ip.dst,
                    'pipe_name': filename,
                    'operation': packet.smb2.cmd if hasattr(packet.smb2, 'cmd') else 'Unknown'
                }
                
                named_pipes.append(pipe_info)
    
    return named_pipes
```

#### Monitoring des named pipes

**PowerShell monitoring**
```powershell
# Monitoring des named pipes avec Sysmon
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-Sysmon/Operational"; ID=17,18} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $processName = ($eventData | Where-Object {$_.Name -eq "Image"}).'#text'
    $pipeName = ($eventData | Where-Object {$_.Name -eq "PipeName"}).'#text'
    $eventType = if ($_.Id -eq 17) { "Created" } else { "Connected" }
    
    Write-Host "Process: $processName $eventType pipe: $pipeName"
}
```

### Analyse des connexions distantes

#### RDP Analysis

**Capture RDP**
```bash
# Capture du trafic RDP
tshark -i eth0 -f "port 3389" -w rdp_traffic.pcap

# Analyse des connexions
tshark -r rdp_traffic.pcap -Y "rdp"
```

**Analyse des logs RDP**
```powershell
# Événements de connexion RDP
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-TerminalServices-LocalSessionManager/Operational"; ID=21,22,25} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $user = ($eventData | Where-Object {$_.Name -eq "User"}).'#text'
    $sourceIP = ($eventData | Where-Object {$_.Name -eq "Address"}).'#text'
    $sessionID = ($eventData | Where-Object {$_.Name -eq "SessionID"}).'#text'
    
    $eventType = switch ($_.Id) {
        21 { "Logon Success" }
        22 { "Shell Start" }
        25 { "Reconnection" }
    }
    
    Write-Host "$eventType - User: $user from IP: $sourceIP (Session: $sessionID)"
}
```

#### WinRM Analysis

**Analyse WinRM**
```powershell
# Événements WinRM
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-WinRM/Operational"} | Where-Object {$_.LevelDisplayName -eq "Information"} | ForEach-Object {
    Write-Host "Time: $($_.TimeCreated) - Message: $($_.Message)"
}

# Analyse des connexions PowerShell remotes
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-PowerShell/Operational"; ID=4103} | ForEach-Object {
    $event = [xml]$_.ToXml()
    Write-Host "PowerShell Remote Command: $($event.Event.EventData.Data.'#text')"
}
```

### Détection de mouvements latéraux

#### Pass-the-Hash Detection

**Analyse des événements d'authentification**
```powershell
# Détection de Pass-the-Hash via Event ID 4624
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4624} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $logonType = ($eventData | Where-Object {$_.Name -eq "LogonType"}).'#text'
    $authPackage = ($eventData | Where-Object {$_.Name -eq "AuthenticationPackageName"}).'#text'
    $targetUser = ($eventData | Where-Object {$_.Name -eq "TargetUserName"}).'#text'
    $sourceIP = ($eventData | Where-Object {$_.Name -eq "IpAddress"}).'#text'
    
    # Logon type 3 (Network) avec NTLM peut indiquer Pass-the-Hash
    if ($logonType -eq "3" -and $authPackage -eq "NTLM") {
        Write-Host "Potential Pass-the-Hash: User $targetUser from IP $sourceIP"
    }
}
```

#### Golden Ticket Detection

**Analyse Kerberos**
```powershell
# Détection de Golden Ticket via Event ID 4769
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4769} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $ticketOptions = ($eventData | Where-Object {$_.Name -eq "TicketOptions"}).'#text'
    $encryptionType = ($eventData | Where-Object {$_.Name -eq "TicketEncryptionType"}).'#text'
    $accountName = ($eventData | Where-Object {$_.Name -eq "TargetUserName"}).'#text'
    
    # Ticket options 0x40810000 peut indiquer Golden Ticket
    if ($ticketOptions -eq "0x40810000") {
        Write-Host "Potential Golden Ticket: Account $accountName with encryption $encryptionType"
    }
}
```

#### Détection de DCSync

**Analyse des réplications AD**
```powershell
# Détection de DCSync via Event ID 4662
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4662} | ForEach-Object {
    $event = [xml]$_.ToXml()
    $eventData = $event.Event.EventData.Data
    
    $objectName = ($eventData | Where-Object {$_.Name -eq "ObjectName"}).'#text'
    $accessMask = ($eventData | Where-Object {$_.Name -eq "AccessMask"}).'#text'
    $subjectUser = ($eventData | Where-Object {$_.Name -eq "SubjectUserName"}).'#text'
    
    # Access mask 0x100 (DS-Replication-Get-Changes) peut indiquer DCSync
    if ($accessMask -eq "0x100") {
        Write-Host "Potential DCSync: User $subjectUser accessing $objectName"
    }
}
```

## Outils d'analyse réseau

### Wireshark avancé

**Filtres utiles**
```
# Trafic suspect
tcp.flags.syn==1 and tcp.flags.ack==0 and tcp.window_size <= 1024

# Connexions longues
tcp.time_delta > 300

# Transferts de données importants
tcp.len > 1000

# Trafic non standard
not (tcp.port == 80 or tcp.port == 443 or tcp.port == 53 or tcp.port == 22)
```

### Zeek (Bro)

**Configuration Zeek**
```zeek
# local.zeek
@load base/frameworks/notice
@load base/protocols/conn
@load base/protocols/http
@load base/protocols/dns
@load base/protocols/ssl

# Détection de beaconing
event connection_established(c: connection) {
    local duration = c$duration;
    local bytes = c$orig_bytes + c$resp_bytes;
    
    if (duration > 300.0 && bytes < 1000) {
        print fmt("Potential beaconing: %s -> %s:%s", c$id$orig_h, c$id$resp_h, c$id$resp_p);
    }
}
```

### Suricata

**Configuration Suricata**
```yaml
# suricata.yaml
rule-files:
  - suricata.rules
  - emerging-threats.rules

outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types:
        - alert
        - http
        - dns
        - tls
        - files
        - smtp
```

Cette approche méthodique permet une analyse réseau complète pour la détection d'activités malveillantes et la reconstruction d'événements forensiques.