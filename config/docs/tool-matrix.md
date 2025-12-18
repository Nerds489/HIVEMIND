# HIVEMIND Tool Access Matrix

## Overview

This document defines which tools each agent can access, their proficiency levels, and any restrictions.

---

## Development Team Tools

### DEV-001: Architect

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Diagramming** | Mermaid, PlantUML, draw.io | Lucidchart, Excalidraw | - |
| **Documentation** | Markdown, Confluence, Notion | Docusaurus, GitBook | - |
| **IDEs** | VS Code, IntelliJ | Any IDE (read-only) | Direct code commits |
| **Modeling** | C4 Model tools, UML tools | ERD tools, ArchiMate | - |
| **Prototyping** | Figma (view), Swagger Editor | API Blueprint | - |
| **Version Control** | Git (read), GitHub/GitLab | - | Direct pushes to main |

**Tool Commands:**
```bash
# Architecture diagrams
mermaid render architecture.mmd -o architecture.png
plantuml sequence.puml

# API design
swagger-editor serve api.yaml
```

---

### DEV-002: Backend Developer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Languages** | Python, Node.js, Go, Java | Rust, Ruby, PHP | - |
| **Frameworks** | FastAPI, Express, Spring | Django, Flask, Gin | - |
| **Databases** | PostgreSQL, MySQL, MongoDB | Redis, Elasticsearch | Production DB direct |
| **APIs** | REST, GraphQL, gRPC | WebSocket, SOAP | - |
| **Testing** | pytest, Jest, JUnit | Mocha, unittest | - |
| **Containers** | Docker, docker-compose | Podman | Production k8s direct |

**Tool Commands:**
```bash
# Python development
python -m pytest tests/ --cov=src
black src/ --check
mypy src/

# Node.js development
npm run test
npm run lint
npm run build

# Database
psql -h localhost -U user -d database
mongosh mongodb://localhost/db
```

---

### DEV-003: Frontend Developer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Frameworks** | React, Vue.js, Next.js | Angular, Svelte | - |
| **Languages** | TypeScript, JavaScript | HTML, CSS, SCSS | - |
| **Build Tools** | Webpack, Vite, esbuild | Rollup, Parcel | - |
| **Testing** | Jest, React Testing Library | Cypress, Playwright | - |
| **Styling** | Tailwind CSS, CSS Modules | Styled Components, SASS | - |
| **Design** | Figma (view), Storybook | Chromatic, Zeplin | Direct Figma edits |

**Tool Commands:**
```bash
# React development
npm run dev
npm run test -- --coverage
npm run build

# Linting and formatting
eslint src/ --fix
prettier --write "src/**/*.{ts,tsx}"

# Storybook
npm run storybook
```

---

### DEV-004: Code Reviewer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Static Analysis** | SonarQube, ESLint, Pylint | Checkstyle, RuboCop | - |
| **Security Scanning** | Semgrep, Bandit, npm audit | Snyk (read), Dependabot | Exploitation |
| **Code Review** | GitHub PR, GitLab MR | Crucible, Gerrit | Merge without approval |
| **Metrics** | Code Climate, SonarQube | - | - |
| **IDEs** | VS Code, IntelliJ | Any IDE | - |
| **Documentation** | Markdown | - | - |

**Tool Commands:**
```bash
# Static analysis
sonar-scanner
eslint . --format json > eslint-report.json
pylint src/ --output-format=json > pylint-report.json

# Security scanning
semgrep --config auto .
bandit -r src/ -f json -o bandit-report.json
npm audit --json > npm-audit.json
```

---

### DEV-005: Technical Writer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Documentation** | Markdown, reStructuredText | AsciiDoc, LaTeX | - |
| **Platforms** | Docusaurus, MkDocs, GitBook | Confluence, Notion | Admin access |
| **API Docs** | Swagger/OpenAPI, Redoc | Slate, API Blueprint | - |
| **Diagrams** | Mermaid, PlantUML | draw.io, Lucidchart | - |
| **Version Control** | Git | - | Force push |
| **Spell Check** | aspell, languagetool | Grammarly | - |

**Tool Commands:**
```bash
# Documentation build
mkdocs build
docusaurus build

# API docs generation
redoc-cli bundle openapi.yaml -o api-docs.html
swagger-codegen generate -i api.yaml -l html2

# Spell check
aspell check document.md
```

---

### DEV-006: DevOps Liaison

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **CI/CD** | GitHub Actions, Jenkins, GitLab CI | CircleCI, Travis CI | Production pipelines |
| **Containers** | Docker, Kubernetes | Podman, Docker Swarm | Prod cluster direct |
| **IaC** | Terraform (dev), CloudFormation | Pulumi, CDK | Production infra |
| **Monitoring** | Prometheus, Grafana | Datadog, New Relic | Alert silencing |
| **Scripting** | Bash, Python | PowerShell | - |
| **Artifact Registry** | Docker Hub, ECR, GCR | Artifactory, Nexus | - |

**Tool Commands:**
```bash
# CI/CD
gh workflow run deploy.yml
jenkins-cli build job/deploy

# Container operations
docker build -t app:latest .
docker push registry/app:latest
kubectl apply -f k8s/dev/

# Terraform (non-prod)
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```

---

## Security Team Tools

### SEC-001: Security Architect

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Threat Modeling** | STRIDE, Threat Dragon | PASTA, OCTAVE | - |
| **Frameworks** | NIST, MITRE ATT&CK | CIS Controls, OWASP | - |
| **Risk Assessment** | Custom risk matrices | FAIR | - |
| **Documentation** | Markdown, Confluence | - | - |
| **Review** | Architecture diagrams | Security scan results | Exploit execution |

**Tool Commands:**
```bash
# Threat modeling
threat-dragon-cli analyze threat-model.json

# MITRE ATT&CK mapping
attack-navigator export attack-map.json
```

---

### SEC-002: Penetration Tester

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Web Testing** | Burp Suite, OWASP ZAP | Nikto, w3af | Unauthorized targets |
| **Network** | Nmap, Masscan, Wireshark | Responder, Impacket | Production without auth |
| **Exploitation** | Metasploit, custom scripts | Cobalt Strike (licensed) | Persistent access |
| **Password** | Hashcat, John the Ripper | Hydra, Medusa | Real credential stuffing |
| **Enumeration** | ffuf, Gobuster, Amass | Subfinder, dnsrecon | - |
| **Reporting** | Markdown, custom templates | Dradis, Faraday | - |

**Tool Commands:**
```bash
# Reconnaissance
nmap -sV -sC -oA scan target.com
masscan -p1-65535 target.com --rate=1000
amass enum -d target.com

# Web testing
ffuf -w wordlist.txt -u https://target.com/FUZZ
sqlmap -u "http://target.com/page?id=1" --batch

# Exploitation (authorized only)
msfconsole -x "use exploit/multi/handler"
```

---

### SEC-003: Malware Analyst

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Disassembly** | Ghidra, IDA Pro | Radare2, Binary Ninja | - |
| **Debugging** | x64dbg, GDB | OllyDbg, WinDbg | - |
| **Sandbox** | Any.run, Cuckoo | Joe Sandbox, VMRay | Live malware release |
| **YARA** | YARA, yarGen | - | - |
| **Network** | Wireshark, Zeek | NetworkMiner | - |
| **Reporting** | Markdown | STIX/TAXII | - |

**Tool Commands:**
```bash
# Static analysis
file malware.bin
strings -a malware.bin > strings.txt
yara -r rules/ malware.bin

# Dynamic analysis (sandbox only)
cuckoo submit malware.bin
```

---

### SEC-004: Wireless Security Expert

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **WiFi** | Aircrack-ng, Kismet | WiFi Pineapple, Bettercap | Unauthorized networks |
| **Bluetooth** | Ubertooth, btlejack | Wireshark (BT), hcitool | - |
| **SDR** | HackRF, RTL-SDR | YARD Stick One | Licensed frequencies |
| **Analysis** | Wireshark | - | - |
| **Reporting** | Markdown | - | - |

**Tool Commands:**
```bash
# WiFi assessment (authorized only)
airmon-ng start wlan0
airodump-ng wlan0mon
aireplay-ng -0 1 -a [BSSID] wlan0mon

# Bluetooth scanning
hcitool scan
btlejack -d [TARGET]
```

---

### SEC-005: Compliance Auditor

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Frameworks** | SOC2, PCI-DSS, HIPAA | GDPR, ISO 27001, NIST | - |
| **Assessment** | Spreadsheets, checklists | GRC platforms | System changes |
| **Evidence** | Screenshots, logs, exports | Document management | - |
| **Reporting** | Markdown, Word | PDF generation | - |
| **Tracking** | Jira, spreadsheets | ServiceNow | - |

**Tool Commands:**
```bash
# Evidence collection
aws cloudtrail lookup-events --output json > cloudtrail.json
gh api /repos/org/repo/actions/runs > github-audit.json
```

---

### SEC-006: Incident Responder

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **SIEM** | Splunk, Elastic SIEM | QRadar, Chronicle | - |
| **Forensics** | Volatility, Autopsy | FTK, EnCase | Evidence tampering |
| **EDR** | CrowdStrike, Carbon Black | SentinelOne, Defender | - |
| **Network** | Wireshark, Zeek | tcpdump, Arkime | - |
| **Scripting** | Python, PowerShell | Bash | - |
| **Communication** | Slack, PagerDuty | - | - |

**Tool Commands:**
```bash
# Memory forensics
volatility -f memory.dmp imageinfo
volatility -f memory.dmp --profile=Win10x64 pslist

# Log analysis
grep -r "ERROR" /var/log/ > errors.txt
splunk search "index=main error" -output json
```

---

## Infrastructure Team Tools

### INF-001: Infrastructure Architect

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Cloud** | AWS, Azure, GCP | DigitalOcean, Linode | Direct prod changes |
| **IaC** | Terraform, CloudFormation | Pulumi, CDK | - |
| **Diagramming** | Diagrams (Python), draw.io | Lucidchart | - |
| **Cost Analysis** | AWS Cost Explorer, Azure Cost | Infracost | - |
| **Documentation** | Markdown, Confluence | - | - |

**Tool Commands:**
```bash
# Infrastructure diagrams
python diagrams/infrastructure.py

# Cost analysis
infracost breakdown --path=terraform/
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31
```

---

### INF-002: Systems Administrator

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **OS** | Linux (RHEL, Ubuntu), Windows Server | macOS | - |
| **Config Management** | Ansible, Puppet | Chef, SaltStack | - |
| **Monitoring** | Nagios, Zabbix | Datadog agent | - |
| **Shell** | Bash, PowerShell | Zsh, Fish | - |
| **Security** | SELinux, AppArmor | CIS benchmarks | Security policy bypass |

**Tool Commands:**
```bash
# System administration
systemctl status nginx
journalctl -u nginx -f
ansible-playbook -i inventory site.yml

# Security hardening
lynis audit system
```

---

### INF-003: Network Engineer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Routing** | Cisco IOS, Junos | VyOS, MikroTik | Internet-facing solo |
| **Firewalls** | pfSense, iptables | AWS Security Groups | - |
| **DNS** | BIND, Route53 | Cloudflare, PowerDNS | - |
| **Analysis** | Wireshark, tcpdump | MTR, traceroute | - |
| **Load Balancing** | HAProxy, NGINX | AWS ALB/NLB | - |

**Tool Commands:**
```bash
# Network diagnostics
traceroute target.com
mtr -r target.com
dig @8.8.8.8 target.com

# Firewall management
iptables -L -n -v
pfctl -sr
```

---

### INF-004: Database Administrator

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **RDBMS** | PostgreSQL, MySQL | Oracle, SQL Server | Schema drops (no backup) |
| **NoSQL** | MongoDB, Redis | Elasticsearch, Cassandra | - |
| **Tools** | pgAdmin, DBeaver | DataGrip, MySQL Workbench | - |
| **Backup** | pg_dump, mysqldump | WAL-E, Percona XtraBackup | Backup deletion |
| **Monitoring** | pg_stat_statements | PMM, pgwatch2 | - |

**Tool Commands:**
```bash
# PostgreSQL
psql -c "SELECT * FROM pg_stat_activity"
pg_dump -Fc database > backup.dump
pg_restore -d database backup.dump

# MySQL
mysqldump --all-databases > backup.sql
mysql -e "SHOW PROCESSLIST"
```

---

### INF-005: Site Reliability Engineer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Monitoring** | Prometheus, Grafana | Datadog, New Relic | Alert silencing (>1hr) |
| **Alerting** | PagerDuty, OpsGenie | Slack alerts | - |
| **Logging** | ELK Stack, Loki | Splunk, Datadog Logs | - |
| **Tracing** | Jaeger, Zipkin | Datadog APM | - |
| **Orchestration** | Kubernetes, Nomad | Docker Swarm | - |
| **SLO** | Prometheus, custom | Nobl9, Blameless | SLO changes solo |

**Tool Commands:**
```bash
# Kubernetes operations
kubectl get pods -n production
kubectl logs -f deployment/app -n production
kubectl rollout status deployment/app

# Prometheus queries
promtool query instant http://prometheus:9090 'up{job="app"}'
```

---

### INF-006: Automation Engineer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **IaC** | Terraform, Ansible | Pulumi, CloudFormation | Production apply solo |
| **Scripting** | Python, Bash | Go, PowerShell | - |
| **CI/CD** | GitHub Actions, Jenkins | GitLab CI, CircleCI | - |
| **Testing** | Terratest, Molecule | InSpec, ServerSpec | - |
| **Version Control** | Git | - | Force push to main |

**Tool Commands:**
```bash
# Terraform
terraform init
terraform plan -out=plan.tfplan
terraform apply plan.tfplan

# Ansible
ansible-playbook -i inventory playbook.yml --check
ansible-playbook -i inventory playbook.yml

# Testing
molecule test
terratest -v ./tests/
```

---

## QA Team Tools

### QA-001: QA Architect

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Strategy** | Test plans, matrices | TestRail, Xray | - |
| **Metrics** | Coverage reports | SonarQube, Code Climate | - |
| **Documentation** | Markdown, Confluence | - | - |
| **Coordination** | Jira, GitHub Issues | - | - |

---

### QA-002: Test Automation Engineer

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **UI Testing** | Selenium, Playwright | Cypress, Puppeteer | Production execution |
| **API Testing** | Postman, REST Assured | Newman, Karate | - |
| **Unit Testing** | Jest, pytest, JUnit | Mocha, unittest | - |
| **CI Integration** | GitHub Actions, Jenkins | CircleCI, GitLab CI | - |
| **Reporting** | Allure, HTML reports | - | - |

**Tool Commands:**
```bash
# Selenium/Playwright
npx playwright test
pytest tests/ --html=report.html

# API testing
newman run collection.json -r cli,html
```

---

### QA-003: Performance Tester

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Load Testing** | JMeter, k6, Gatling | Locust, Artillery | Prod load without approval |
| **APM** | Datadog APM, New Relic | Dynatrace | - |
| **Profiling** | async-profiler, py-spy | - | - |
| **Reporting** | Grafana, custom | - | - |

**Tool Commands:**
```bash
# k6 load testing
k6 run --vus 100 --duration 5m script.js

# JMeter
jmeter -n -t test.jmx -l results.jtl -e -o report/
```

---

### QA-004: Security Tester

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **SAST** | SonarQube, Semgrep | Checkmarx, Fortify | - |
| **DAST** | OWASP ZAP, Burp (automated) | Nikto | Exploitation |
| **SCA** | Snyk, Dependabot | WhiteSource, Black Duck | - |
| **Container** | Trivy, Clair | Anchore | - |
| **Secrets** | TruffleHog, git-secrets | detect-secrets | - |

**Tool Commands:**
```bash
# SAST scanning
semgrep --config auto --json > sast-results.json
sonar-scanner

# Dependency scanning
snyk test --json > snyk-results.json
trivy image app:latest -f json > trivy-results.json
```

---

### QA-005: Manual QA Tester

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Bug Tracking** | Jira, GitHub Issues | Bugzilla, Linear | - |
| **Test Management** | TestRail, Zephyr | Xray, qTest | - |
| **Screen Capture** | Loom, Screenshots | - | - |
| **Browsers** | Chrome, Firefox, Safari | Edge, mobile browsers | - |
| **Devices** | BrowserStack, real devices | Sauce Labs | - |

---

### QA-006: Test Data Manager

| Tool Category | Primary Tools | Secondary Tools | Restricted |
|---------------|---------------|-----------------|------------|
| **Data Generation** | Faker, custom scripts | Mockaroo | - |
| **Data Masking** | Delphix, custom | Informatica | Production data export |
| **Databases** | psql, mysql, mongosh | - | Production direct |
| **Environments** | Docker, Kubernetes | Vagrant | - |

**Tool Commands:**
```bash
# Data generation
python generate_test_data.py --count 1000 --output data.json

# Data masking
pg_dump production | sed 's/email@/masked@/g' > masked.sql
```

---

## Tool Access Legend

| Symbol | Meaning |
|--------|---------|
| Primary | Regularly used, high proficiency expected |
| Secondary | Occasionally used, working knowledge |
| Restricted | Cannot use without explicit approval or supervision |
