# 🤖 Asistente Virtual Rasa en AWS (t3.small)

Este repositorio contiene un agente Rasa que consulta el estado de un flujo de negocio a partir de un `NIT`, usando una Lambda expuesta mediante API Gateway. Está optimizado para ser desplegado en una instancia EC2 tipo `t3.small`.

---

## 🚀 Requisitos

- Cuenta de AWS
- Par de llaves EC2 (`.pem`)
- Instancia EC2 Ubuntu 22.04 LTS (`t3.small`)
- Docker y Docker Compose
- Rasa CLI (opcional para desarrollo local)

---

## 🏗️ Estructura del proyecto

```
rasa-agente/
├── actions/              # Código Python para acciones personalizadas
│   └── actions.py
├── data/                 # Intenciones y historias
│   ├── nlu.yml
│   └── stories.yml
├── config.yml            # Pipeline de procesamiento NLP
├── credentials.yml       # Configuración de canales
├── domain.yml            # Definición de intents, slots, respuestas
├── docker-compose.yml    # Contenedores para Rasa y action server
├── endpoints.yml         # Conexión entre Rasa y action server
└── models/               # (Vacío) se llena al entrenar
```

---

## ⚙️ Paso a paso para desplegar en EC2

### 1. Conéctate a tu instancia EC2

```bash
ssh -i "tu-llave.pem" ubuntu@<IP_PUBLICA>
# `tu-llave.pem` hace referencia a la llave generada por EC2
```

### 2. Instala Docker y Docker Compose

```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
newgrp docker
```

### 3. Sube el proyecto

Desde tu máquina local:

```bash
scp -i "tu-llave.pem" rasa_agente_completo.zip ubuntu@<IP_PUBLICA>:~/
```

En EC2:

```bash
unzip rasa_agente_completo.zip
cd rasa_agente
```

### 4. (Opcional) Habilita memoria swap

```bash
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 5. Levanta los servicios

```bash
docker-compose up -d
```

### 6. Verifica

```bash
curl http://localhost:5005/status
```

---

## 🧪 Entrenar modelo local (opcional)

```bash
rasa train
# Subir el archivo generado a la carpeta models/ del servidor
```

---

## 🧠 ¿Qué hace el bot?

1. El usuario pregunta por un `NIT`
2. El bot llama a una API Gateway
3. La API consulta en Lambda dos tablas de DynamoDB:
   - `FlujosCliente`: flujo en ejecución
   - `ErroresDetalle`: detalles del código de error
4. El bot responde con un diagnóstico detallado

---

