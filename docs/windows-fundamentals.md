# Windows Fundamentals for Digital Forensics

## Architecture Windows - Compréhension du système

### Structure du kernel Windows

Le noyau Windows est organisé en plusieurs couches qui gèrent les ressources système et fournissent une interface entre les applications et le matériel.

#### Composants principaux du kernel

**Executive Layer**
- **Object Manager** : Gère tous les objets système (processus, threads, fichiers, etc.)
- **Memory Manager** : Gestion de la mémoire virtuelle et physique
- **Process Manager** : Création et gestion des processus et threads
- **I/O Manager** : Gestion des entrées/sorties et du système de fichiers
- **Security Reference Monitor** : Contrôle d'accès et audit de sécurité

**HAL (Hardware Abstraction Layer)**
- Interface entre le kernel et le matériel
- Abstraction des spécificités matérielles
- Gestion des interruptions et de l'accès aux périphériques

**Kernel Layer**
- Ordonnancement des threads (dispatcher)
- Gestion des interruptions et exceptions
- Synchronisation des objets kernel

### Gestion des processus et threads

#### Structure des processus

**Process Block (EPROCESS)**
```
- Process ID (PID)
- Parent Process ID (PPID)
- Token de sécurité
- Espace d'adressage virtuel
- Liste des threads
- Handles ouverts
- Informations de session
```

**Thread Block (ETHREAD)**
```
- Thread ID (TID)
- État du thread (Running, Ready, Waiting)
- Priorité et scheduling
- Contexte CPU
- Stack kernel et user
```

#### Cycle de vie des processus

1. **Création** : `CreateProcess()` → `NtCreateProcess()`
2. **Initialisation** : Chargement de l'exécutable et des DLLs
3. **Exécution** : Ordonnancement des threads
4. **Terminaison** : Libération des ressources

#### Artefacts forensiques

**Processus cachés**
- Techniques de détection (VAD traversal)
- Analyse des structures EPROCESS
- Comparaison avec la liste des processus visible

**Injection de code**
- DLL injection
- Process hollowing
- Reflective DLL loading

### Modèle de sécurité Windows

#### Tokens de sécurité

**Structure du token**
```
- User SID
- Group SIDs
- Privileges
- Logon Session ID
- Token Type (Primary/Impersonation)
- Integrity Level
```

**Types de tokens**
- **Primary Token** : Attaché au processus
- **Impersonation Token** : Temporaire pour un thread

#### Contrôle d'accès

**Security Descriptors**
- **Owner** : Propriétaire de l'objet
- **DACL** (Discretionary Access Control List)
- **SACL** (System Access Control List)

**Access Control Entries (ACE)**
```
- Type (Allow/Deny)
- Inheritance flags
- Access mask
- Security Identifier (SID)
```

#### Audit et logging

**Event Logs**
- Security Log : Authentification, accès aux objets
- System Log : Événements système
- Application Log : Applications tierces

**Audit Policy**
- Object Access
- Logon Events
- Account Management
- Policy Changes

### Services et démons système

#### Architecture des services

**Service Control Manager (SCM)**
- Base de données des services
- Démarrage et arrêt des services
- Gestion des dépendances

**Service Types**
- **Win32 Service** : Service standard
- **Kernel Driver** : Pilote en mode kernel
- **File System Driver** : Pilote système de fichiers

#### Persistance via les services

**Méthodes d'installation**
```powershell
# Création d'un service
sc create malware binPath= "C:\malware.exe" start= auto

# Modification d'un service existant
sc config Spooler binPath= "C:\malware.exe"
```

**Détection forensique**
- Analyse du registre `HKLM\SYSTEM\CurrentControlSet\Services`
- Vérification des binaires de services
- Corrélation avec les logs d'événements

## Internals Windows pour DFIR - Concepts avancés

### Object Manager et Handle Table

#### Architecture des objets

**Object Types**
```
- Process
- Thread
- File
- Registry Key
- Token
- Event
- Mutex
- Semaphore
```

**Object Header**
```
- Object Type
- Reference Count
- Handle Count
- Name
- Security Descriptor
```

#### Handle Table

**Structure**
- Table par processus
- Index vers Object Pointer
- Access Rights
- Inherit Flag

**Analyse forensique**
```python
# Pseudo-code pour l'analyse des handles
for process in processes:
    for handle in process.handles:
        object_type = handle.object.type
        object_name = handle.object.name
        access_rights = handle.access_rights
```

### Windows API et syscalls

#### Transition User Mode → Kernel Mode

**Séquence d'appel**
1. Application → Win32 API (kernel32.dll)
2. Win32 API → Native API (ntdll.dll)
3. Native API → System Call (syscall)
4. Kernel → Executive Functions

**Hooking et détection**
- **User-mode hooks** : IAT/EAT hooking
- **Kernel-mode hooks** : SSDT hooking
- **Techniques de détection** : Vérification d'intégrité des tables

#### Syscalls importants pour DFIR

**Gestion des fichiers**
- `NtCreateFile`
- `NtReadFile`
- `NtWriteFile`
- `NtDeleteFile`

**Gestion des processus**
- `NtCreateProcess`
- `NtTerminateProcess`
- `NtReadVirtualMemory`
- `NtWriteVirtualMemory`

**Gestion du registre**
- `NtCreateKey`
- `NtSetValueKey`
- `NtQueryValueKey`
- `NtDeleteKey`

### Gestion des DLLs et modules

#### Chargement des DLLs

**Process Environment Block (PEB)**
```
- Image Base Address
- Ldr (Loader Data)
- Process Parameters
- Module List
```

**Loader Data**
- InLoadOrderModuleList
- InMemoryOrderModuleList
- InInitializationOrderModuleList

#### Techniques de persistance

**DLL Hijacking**
- Search Order Hijacking
- Phantom DLL Hijacking
- DLL Side-loading

**Détection forensique**
```python
# Vérification des DLLs chargées
for module in process.modules:
    if module.path not in trusted_paths:
        check_digital_signature(module.path)
        analyze_module_imports(module)
```

### Mécanismes de persistence

#### Registre Windows

**Clés de démarrage automatique**
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunServices
```

**Services**
```
HKLM\SYSTEM\CurrentControlSet\Services
```

**Winlogon**
```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
- Shell
- Userinit
- Notify
```

#### Scheduled Tasks

**Stockage**
```
%SystemRoot%\System32\Tasks
%SystemRoot%\Tasks (Windows XP/2003)
```

**Analyse forensique**
- Parsing des fichiers de tâches
- Corrélation avec les logs d'événements
- Vérification des triggers et actions

#### WMI (Windows Management Instrumentation)

**Persistance via WMI**
```powershell
# Event Consumer
$consumer = Set-WmiInstance -Namespace "root\subscription" -Class "CommandLineEventConsumer" -Arguments @{
    Name = "MalwareConsumer"
    CommandLineTemplate = "C:\malware.exe"
}

# Event Filter
$filter = Set-WmiInstance -Namespace "root\subscription" -Class "__EventFilter" -Arguments @{
    Name = "MalwareFilter"
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfRawData_PerfOS_System'"
}

# Binding
Set-WmiInstance -Namespace "root\subscription" -Class "__FilterToConsumerBinding" -Arguments @{
    Filter = $filter
    Consumer = $consumer
}
```

**Détection**
- Énumération des Event Consumers
- Analyse des requêtes WQL suspectes
- Vérification des bindings

## Points clés pour l'analyse forensique

### Artefacts essentiels

1. **Mémoire système**
   - Structures EPROCESS/ETHREAD
   - VAD (Virtual Address Descriptors)
   - Handle Tables
   - Object Manager

2. **Registre Windows**
   - Clés de persistance
   - Configuration des services
   - Historique des activités

3. **Logs système**
   - Event Logs
   - ETW traces
   - Audit logs

### Outils recommandés

- **Volatility** : Analyse mémoire
- **Registry Explorer** : Analyse du registre
- **Process Monitor** : Monitoring temps réel
- **Autoruns** : Détection de persistance
- **WinAPIOverride** : Monitoring des API calls

Cette compréhension des fondamentaux Windows est essentielle pour toute analyse forensique efficace sur les systèmes Windows.