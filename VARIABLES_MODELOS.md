# Variables de los Modelos de Prediccion

**Sistema de Prediccion de Incidentes de Ciberseguridad**

Este documento describe las variables dependientes e independientes de cada modelo de Machine Learning del sistema.

---

## Indice

1. [Resumen Comparativo](#resumen-comparativo)
2. [Phishing Email Detection](#1-phishing-email-detection)
3. [Account Takeover Detection](#2-account-takeover-ato-detection)
4. [Brute Force Detection](#3-brute-force-detection)
5. [Anexo: Lista Completa de Features](#anexo-lista-completa-de-features)
6. [Importancia de Variables en la Vida Real](#importancia-de-variables-en-la-vida-real)

---

## Resumen Comparativo

| Aspecto | Phishing | ATO | Brute Force |
|---------|----------|-----|-------------|
| **Variable Dependiente** | `label` | `Is Account Takeover` | `Label` |
| **Tipo Target** | Binario (0/1) | Binario (0/1) | Binario (0/1) |
| **Total Features** | 1,016 | 35 | 60 |
| **Balance Dataset** | 44% vs 56% | 0.17% vs 99.83% | 50% vs 50% |
| **Tipo de Datos** | Texto (emails) | Comportamental | Flujo de red |
| **Algoritmo** | Gradient Boosting | Gradient Boosting | Random Forest |
| **F1-Score** | 99.01% | 75.86% | 99.97% |

---

## 1. Phishing Email Detection

### Variable Dependiente (Target)

| Campo | Descripcion |
|-------|-------------|
| **Nombre** | `label` |
| **Tipo** | Binario |
| **Valores** | 0 = Legitimo, 1 = Phishing |
| **Distribucion** | 44% Legitimo / 56% Phishing |

### Variables Independientes

**Total: 1,016 features** compuestas por:
- 16 features numericas derivadas
- 1,000 features TF-IDF (vectorizacion de texto)

#### Features Numericas (16)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `subject_length` | Longitud del asunto en caracteres |
| 2 | `subject_words` | Conteo de palabras en el asunto |
| 3 | `subject_special` | Conteo de caracteres especiales en asunto |
| 4 | `body_length` | Longitud del cuerpo del email |
| 5 | `body_words` | Conteo de palabras en el cuerpo |
| 6 | `body_special` | Conteo de caracteres especiales en cuerpo |
| 7 | `url_count` | Cantidad de URLs detectadas |
| 8 | `urls` | Indicador binario de presencia de URLs |
| 9 | `sender_domain_encoded` | Dominio del remitente codificado (top 50) |
| 10 | `subject_sentiment` | Score de sentimiento del asunto (0-1) |
| 11 | `body_sentiment` | Score de sentimiento del cuerpo (0-1) |
| 12 | `subject_body_ratio` | Ratio longitud asunto/cuerpo |
| 13 | `special_chars_ratio` | Ratio de caracteres especiales |
| 14 | `has_urgent` | Flag: contiene "urgent/urgente" |
| 15 | `has_free` | Flag: contiene "free/gratis" |
| 16 | `has_click` | Flag: contiene "click here/haz clic" |

#### Features TF-IDF (1,000)

- **Nombres**: `tfidf_0`, `tfidf_1`, ..., `tfidf_999`
- **Fuente**: Texto combinado de subject + body
- **Configuracion**:
  - `max_features`: 1,000
  - `ngram_range`: (1, 2) - unigramas y bigramas
  - `min_df`: 5
  - `stop_words`: English

### Datos de Entrada (Raw)

| Columna | Descripcion | Usado en Features |
|---------|-------------|-------------------|
| `sender` | Email del remitente | Si (dominio) |
| `receiver` | Email del destinatario | No |
| `date` | Fecha del email | No |
| `subject` | Asunto del email | Si |
| `body` | Cuerpo del email | Si |
| `urls` | Indicador de URLs | Si |
| `label` | Target | - |

---

## 2. Account Takeover (ATO) Detection

### Variable Dependiente (Target)

| Campo | Descripcion |
|-------|-------------|
| **Nombre** | `Is Account Takeover` |
| **Tipo** | Binario |
| **Valores** | 0 = Normal, 1 = Account Takeover |
| **Distribucion** | 99.83% Normal / 0.17% ATO (muy desbalanceado) |

### Variables Independientes

**Total: 35 features** en 5 categorias:

#### A. Features Temporales (7)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `hour` | Hora del login (0-23) |
| 2 | `day_of_week` | Dia de la semana (0=Lunes, 6=Domingo) |
| 3 | `day_of_month` | Dia del mes (1-31) |
| 4 | `month` | Mes (1-12) |
| 5 | `is_weekend` | Flag: es sabado o domingo |
| 6 | `is_night` | Flag: entre 22:00 y 06:00 |
| 7 | `is_business_hours` | Flag: entre 09:00 y 17:00 |

#### B. Features de Comportamiento (8)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `ip_changed` | Flag: IP cambio vs login anterior |
| 2 | `country_changed` | Flag: pais cambio vs login anterior |
| 3 | `browser_changed` | Flag: navegador cambio vs login anterior |
| 4 | `device_changed` | Flag: dispositivo cambio vs login anterior |
| 5 | `os_changed` | Flag: SO cambio vs login anterior |
| 6 | `time_since_last_login_hours` | Horas desde ultimo login |
| 7 | `is_rapid_login` | Flag: login en menos de 1 hora |
| 8 | `is_long_gap` | Flag: gap mayor a 24 horas |

#### C. Features Agregados por Usuario (6)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `ip_count_per_user` | IPs unicas usadas por el usuario |
| 2 | `country_count_per_user` | Paises unicos del usuario |
| 3 | `browser_count_per_user` | Navegadores unicos del usuario |
| 4 | `device_count_per_user` | Dispositivos unicos del usuario |
| 5 | `total_logins_per_user` | Total de logins del usuario |
| 6 | `success_rate_per_user` | Tasa de exito de logins |

#### D. Features de Red/IP (4)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `user_count_per_ip` | Usuarios unicos desde esta IP |
| 2 | `is_suspicious_ip` | Flag: IP con mas de 10 usuarios |
| 3 | `rtt_zscore` | Z-score de Round-Trip Time |
| 4 | `is_abnormal_rtt` | Flag: RTT anormal (>2 std) |

#### E. Features Categoricos Encoded (6)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Browser Name and Version_encoded` | Navegador codificado |
| 2 | `OS Name and Version_encoded` | Sistema operativo codificado |
| 3 | `Device Type_encoded` | Tipo de dispositivo codificado |
| 4 | `Country_encoded` | Pais codificado |
| 5 | `Region_encoded` | Region codificada |
| 6 | `City_encoded` | Ciudad codificada |

#### F. Features Numericas Originales (4)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Round-Trip Time [ms]` | Latencia de red en milisegundos |
| 2 | `ASN` | Autonomous System Number |
| 3 | `Login Successful` | Flag de login exitoso |
| 4 | `Is Attack IP` | Flag de IP en lista negra |

### Datos de Entrada (Raw)

| Columna | Descripcion | Usado en Features |
|---------|-------------|-------------------|
| `index` | ID del registro | No |
| `Login Timestamp` | Timestamp del login | Si (temporales) |
| `User ID` | ID del usuario | Si (agregados) |
| `Round-Trip Time [ms]` | Latencia | Si |
| `IP Address` | Direccion IP | Si (cambios, agregados) |
| `Country` | Pais | Si |
| `Region` | Region | Si |
| `City` | Ciudad | Si |
| `ASN` | Autonomous System Number | Si |
| `User Agent String` | User Agent completo | No |
| `Browser Name and Version` | Navegador | Si |
| `OS Name and Version` | Sistema Operativo | Si |
| `Device Type` | Tipo de dispositivo | Si |
| `Login Successful` | Login exitoso | Si |
| `Is Attack IP` | IP maliciosa | Si |
| `Is Account Takeover` | Target | - |

### Insight Clave

> **98.6% de los ATOs tienen cambio de pais** - Esta es la feature mas discriminante del modelo.

---

## 3. Brute Force Detection

### Variable Dependiente (Target)

| Campo | Descripcion |
|-------|-------------|
| **Nombre** | `Label` |
| **Tipo** | Binario |
| **Valores** | 0 = Benigno, 1 = Brute Force Attack |
| **Distribucion** | 50% Benigno / 50% Ataque (balanceado) |

### Variables Independientes

**Total: 60 features** de flujo de red (normalizadas 0-1)

#### A. Duracion y Conteo de Paquetes (8)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Flow Duration` | Duracion total del flujo |
| 2 | `Tot Fwd Pkts` | Total paquetes hacia adelante |
| 3 | `Tot Bwd Pkts` | Total paquetes hacia atras |
| 4 | `TotLen Fwd Pkts` | Longitud total paquetes forward |
| 5 | `Fwd Act Data Pkts` | Paquetes de datos activos forward |
| 6 | `Bwd IAT Tot` | Suma total inter-arrival time backward |
| 7 | `Fwd Pkts/s` | Paquetes/segundo forward |
| 8 | `Bwd Pkts/s` | Paquetes/segundo backward |

#### B. Longitud de Paquetes (10)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Fwd Pkt Len Max` | Longitud maxima paquete forward |
| 2 | `Fwd Pkt Len Min` | Longitud minima paquete forward |
| 3 | `Fwd Pkt Len Mean` | Longitud promedio paquete forward |
| 4 | `Fwd Pkt Len Std` | Desviacion std longitud forward |
| 5 | `Bwd Pkt Len Max` | Longitud maxima paquete backward |
| 6 | `Bwd Pkt Len Min` | Longitud minima paquete backward |
| 7 | `Bwd Pkt Len Mean` | Longitud promedio paquete backward |
| 8 | `Bwd Pkt Len Std` | Desviacion std longitud backward |
| 9 | `Pkt Len Mean` | Promedio longitud todos los paquetes |
| 10 | `Pkt Len Std` | Desviacion std todos los paquetes |

#### C. Velocidad y Tasas (6)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Flow Byts/s` | Bytes/segundo en el flujo |
| 2 | `Flow Pkts/s` | Paquetes/segundo en el flujo |
| 3 | `Flow IAT Mean` | Inter-arrival time promedio |
| 4 | `Flow IAT Std` | Inter-arrival time desviacion std |
| 5 | `Flow IAT Max` | Inter-arrival time maximo |
| 6 | `Fwd IAT Std` | IAT desviacion std forward |

#### D. Flags TCP (11)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `FIN Flag Cnt` | Conteo de flags FIN |
| 2 | `RST Flag Cnt` | Conteo de flags RST |
| 3 | `PSH Flag Cnt` | Conteo de flags PSH |
| 4 | `ACK Flag Cnt` | Conteo de flags ACK |
| 5 | `URG Flag Cnt` | Conteo de flags URG |
| 6 | `CWE Flag Count` | Conteo de flags CWE |
| 7 | `Fwd PSH Flags` | Flags PSH forward |
| 8 | `Bwd PSH Flags` | Flags PSH backward |
| 9 | `Fwd URG Flags` | Flags URG forward |
| 10 | `Bwd URG Flags` | Flags URG backward |
| 11 | `Down/Up Ratio` | Ratio bytes descarga/subida |

#### E. Inter-Arrival Time (5)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Fwd IAT Std` | IAT desviacion std forward |
| 2 | `Bwd IAT Mean` | IAT promedio backward |
| 3 | `Bwd IAT Std` | IAT desviacion std backward |
| 4 | `Bwd IAT Max` | IAT maximo backward |
| 5 | `Bwd IAT Min` | IAT minimo backward |

#### F. Bytes/Bits y Tasas de Bloque (6)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Fwd Byts/b Avg` | Bytes/bits promedio forward |
| 2 | `Fwd Pkts/b Avg` | Paquetes/bits promedio forward |
| 3 | `Fwd Blk Rate Avg` | Tasa de bloque promedio forward |
| 4 | `Bwd Byts/b Avg` | Bytes/bits promedio backward |
| 5 | `Bwd Pkts/b Avg` | Paquetes/bits promedio backward |
| 6 | `Bwd Blk Rate Avg` | Tasa de bloque promedio backward |

#### G. Ventana TCP (2)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Init Fwd Win Byts` | Bytes ventana inicial forward |
| 2 | `Init Bwd Win Byts` | Bytes ventana inicial backward |

#### H. Actividad/Inactividad (6)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Active Mean` | Promedio tiempo activo |
| 2 | `Active Std` | Desviacion std tiempo activo |
| 3 | `Active Max` | Maximo tiempo activo |
| 4 | `Active Min` | Minimo tiempo activo |
| 5 | `Idle Mean` | Promedio tiempo inactivo |
| 6 | `Idle Std` | Desviacion std tiempo inactivo |

#### I. Otros (6)

| # | Feature | Descripcion |
|---|---------|-------------|
| 1 | `Dst Port` | Puerto de destino |
| 2 | `Protocol` | Protocolo (TCP/UDP) |
| 3 | `Timestamp` | Marca temporal |
| 4 | `Pkt Len Max` | Longitud maxima de paquete |
| 5 | `Pkt Len Var` | Varianza de longitud de paquete |
| 6 | `Fwd Seg Size Min` | Tamano minimo de segmento forward |

### Features mas Discriminantes

| Feature | Ratio Ataque/Normal | Interpretacion |
|---------|---------------------|----------------|
| `Bwd Pkts/s` | 112.7x | Velocidad extrema de bots |
| `Flow Pkts/s` | 24.7x | Ataques automatizados |
| `PSH Flag Cnt` | 1.96x | Firma de herramientas |
| `Flow Duration` | 0.01x | Intentos rapidos |

---

## Anexo: Lista Completa de Features

### Phishing (1,016 features)

**Features Numericas (16):**
```
subject_length, subject_words, subject_special, body_length, body_words,
body_special, url_count, urls, sender_domain_encoded, subject_sentiment,
body_sentiment, subject_body_ratio, special_chars_ratio, has_urgent,
has_free, has_click
```

**Features TF-IDF (1,000):**
```
tfidf_0, tfidf_1, tfidf_2, ..., tfidf_999
```

---

### Account Takeover (35 features)

**Temporales (7):**
```
hour, day_of_week, day_of_month, month, is_weekend, is_night, is_business_hours
```

**Comportamiento (8):**
```
ip_changed, country_changed, browser_changed, device_changed, os_changed,
time_since_last_login_hours, is_rapid_login, is_long_gap
```

**Agregados por Usuario (6):**
```
ip_count_per_user, country_count_per_user, browser_count_per_user,
device_count_per_user, total_logins_per_user, success_rate_per_user
```

**Red/IP (4):**
```
user_count_per_ip, is_suspicious_ip, rtt_zscore, is_abnormal_rtt
```

**Categoricos Encoded (6):**
```
Browser Name and Version_encoded, OS Name and Version_encoded,
Device Type_encoded, Country_encoded, Region_encoded, City_encoded
```

**Numericas Originales (4):**
```
Round-Trip Time [ms], ASN, Login Successful, Is Attack IP
```

---

### Brute Force (60 features)

**Duracion y Conteo (8):**
```
Flow Duration, Tot Fwd Pkts, Tot Bwd Pkts, TotLen Fwd Pkts,
Fwd Act Data Pkts, Bwd IAT Tot, Fwd Pkts/s, Bwd Pkts/s
```

**Longitud de Paquetes (10):**
```
Fwd Pkt Len Max, Fwd Pkt Len Min, Fwd Pkt Len Mean, Fwd Pkt Len Std,
Bwd Pkt Len Max, Bwd Pkt Len Min, Bwd Pkt Len Mean, Bwd Pkt Len Std,
Pkt Len Mean, Pkt Len Std
```

**Velocidad y Tasas (6):**
```
Flow Byts/s, Flow Pkts/s, Flow IAT Mean, Flow IAT Std, Flow IAT Max, Fwd IAT Std
```

**Flags TCP (11):**
```
FIN Flag Cnt, RST Flag Cnt, PSH Flag Cnt, ACK Flag Cnt, URG Flag Cnt,
CWE Flag Count, Fwd PSH Flags, Bwd PSH Flags, Fwd URG Flags,
Bwd URG Flags, Down/Up Ratio
```

**Inter-Arrival Time (5):**
```
Fwd IAT Std, Bwd IAT Mean, Bwd IAT Std, Bwd IAT Max, Bwd IAT Min
```

**Bytes/Bits y Bloque (6):**
```
Fwd Byts/b Avg, Fwd Pkts/b Avg, Fwd Blk Rate Avg,
Bwd Byts/b Avg, Bwd Pkts/b Avg, Bwd Blk Rate Avg
```

**Ventana TCP (2):**
```
Init Fwd Win Byts, Init Bwd Win Byts
```

**Actividad/Inactividad (6):**
```
Active Mean, Active Std, Active Max, Active Min, Idle Mean, Idle Std
```

**Otros (6):**
```
Dst Port, Protocol, Timestamp, Pkt Len Max, Pkt Len Var, Fwd Seg Size Min
```

---

## Importancia de Variables en la Vida Real

Esta seccion explica **en detalle** que significa cada variable, por que es importante para detectar ataques, y como se relaciona con el comportamiento real de los atacantes. Esta basada en investigaciones academicas, reportes de la industria y estudios de ciberseguridad.

---

### 6.1 Phishing Email Detection - Explicacion Detallada

#### Contexto: ¿Que es el Phishing?

El phishing es un ataque donde criminales envian emails falsos haciendose pasar por empresas legitimas (bancos, Netflix, Amazon, etc.) para robar credenciales, datos financieros o instalar malware. Es el **vector de ataque mas comun**: el 80% de los ciberataques comienzan con un email de phishing.

#### Estadisticas que Demuestran la Gravedad

| Estadistica | Valor | Fuente |
|-------------|-------|--------|
| Emails de spoofing enviados diariamente | 3.1 billones | Anti-Phishing Working Group |
| Perdidas globales desde 2016 | $26 billones USD | FBI IC3 |
| Victimas anuales (solo EEUU) | 300,000+ | FTC |
| Ataques que comienzan con email | 80% | Verizon DBIR |

---

#### ¿Que es TF-IDF y Por Que lo Usamos?

**TF-IDF** significa "Term Frequency - Inverse Document Frequency" (Frecuencia de Termino - Frecuencia Inversa de Documento). Es una tecnica matematica para convertir texto en numeros que una computadora puede analizar.

**Explicacion simple:**

Imagina que tienes 1,000 emails y quieres saber que palabras son "sospechosas". TF-IDF hace dos cosas:

1. **TF (Term Frequency)**: Cuenta cuantas veces aparece una palabra en UN email especifico
   - Si un email dice "URGENTE URGENTE URGENTE", la palabra "urgente" tiene TF alto en ese email

2. **IDF (Inverse Document Frequency)**: Penaliza palabras que aparecen en TODOS los emails
   - Palabras como "el", "de", "que" aparecen en casi todos los emails → tienen IDF bajo (no son utiles)
   - Palabras como "suspended", "verify", "winner" aparecen solo en emails sospechosos → tienen IDF alto (muy utiles)

**Formula simplificada:**
```
TF-IDF = (veces que aparece la palabra en este email) × log(total emails / emails que contienen esta palabra)
```

**Ejemplo practico:**

| Palabra | Aparece en email actual | Aparece en % de todos los emails | TF-IDF | Interpretacion |
|---------|-------------------------|----------------------------------|--------|----------------|
| "the" | 5 veces | 95% de emails | 0.02 | Palabra comun, no util |
| "suspended" | 2 veces | 3% de emails | 3.21 | Palabra rara, MUY util |
| "verify" | 3 veces | 5% de emails | 2.89 | Palabra sospechosa |
| "congratulations" | 1 vez | 2% de emails | 3.91 | Tipica de estafas |

**¿Por que TF-IDF es tan efectivo para phishing?**

Los emails de phishing usan un **vocabulario predecible**:
- Urgencia: "immediately", "suspended", "urgent", "action required"
- Premios falsos: "winner", "congratulations", "selected", "prize"
- Suplantacion: "verify", "confirm", "update", "secure"
- Llamadas a accion: "click here", "login now", "download"

TF-IDF detecta automaticamente estas palabras porque aparecen **frecuentemente en phishing pero raramente en emails legitimos**.

**Nuestro modelo usa 1,000 features TF-IDF**, lo que significa que analiza las 1,000 palabras/frases mas discriminantes entre phishing y emails legitimos.

---

#### Explicacion Detallada de Cada Variable de Phishing

##### Variables de IMPORTANCIA CRITICA

**1. `url_count` y `urls` - Conteo y Presencia de Enlaces**

| Aspecto | Explicacion |
|---------|-------------|
| **Que mide** | Cuantos enlaces (URLs) contiene el email y si tiene al menos uno |
| **Por que es critico** | El 75% de los emails de phishing contienen URLs maliciosas. El objetivo del atacante es que hagas clic en un enlace falso |
| **Como atacan** | Usan "typosquatting": dominios casi identicos al real. Ejemplo: `paypa1.com` (con numero 1) en vez de `paypal.com` (con letra L) |
| **Dato real** | Los phishers registran miles de dominios falsos diariamente. Un estudio encontro 100,000+ dominios typosquatting activos |

**Ejemplo de URL maliciosa vs legitima:**
```
LEGITIMO:  https://www.paypal.com/login
PHISHING:  https://www.paypa1.com/login      ← Numero "1" en vez de letra "L"
PHISHING:  https://paypal-secure.com/login   ← Dominio diferente
PHISHING:  https://paypal.com.fake-site.ru/  ← El dominio real es fake-site.ru
```

---

**2. `has_urgent` - Detector de Lenguaje de Urgencia**

| Aspecto | Explicacion |
|---------|-------------|
| **Que mide** | Si el email contiene palabras como "urgent", "urgente", "immediately", "ahora" |
| **Por que es critico** | Los atacantes usan **presion psicologica** para que actues sin pensar. Si te dicen "tienes 24 horas o perderas tu cuenta", entras en panico y no verificas si el email es real |
| **Estadistica** | Presente en >60% de emails de phishing exitosos |
| **Tacticas comunes** | "Tu cuenta sera suspendida en 24 horas", "Accion requerida inmediatamente", "Ultimo aviso antes de cierre" |

**Por que funciona psicologicamente:**

Los humanos bajo presion de tiempo:
- No verifican el remitente
- No revisan la URL antes de hacer clic
- No piensan "¿por que mi banco me pediria esto por email?"

---

**3. `sender_domain_encoded` - Dominio del Remitente Codificado**

| Aspecto | Explicacion |
|---------|-------------|
| **Que mide** | El dominio de quien envia el email (la parte despues del @ en el remitente), convertido a numero |
| **Por que es critico** | El 90%+ de ataques de phishing usan "domain spoofing" - hacerse pasar por empresas legitimas |
| **Como funciona el encoding** | Asignamos numeros a los 50 dominios mas comunes. Gmail=1, Outlook=2, etc. Dominios raros = 0 |
| **Que busca el modelo** | Emails que dicen ser de "Banco X" pero vienen de dominios sospechosos o desconocidos |

**Ejemplo de spoofing:**
```
LEGITIMO:    De: soporte@bancobcp.com.pe
PHISHING:    De: soporte@bancobcp-seguridad.com   ← Dominio falso
PHISHING:    De: bancobcp@gmail.com               ← Banco no usa Gmail
PHISHING:    De: soporte@xn--bancbcp-9za.com      ← Dominio con caracteres unicode
```

---

##### Variables de IMPORTANCIA ALTA

**4. `has_click` - Detector de "Click Here"**

| Aspecto | Explicacion |
|---------|-------------|
| **Que mide** | Si el email contiene frases como "click here", "haz clic aqui", "pulsa aqui" |
| **Por que es importante** | Emails corporativos legitimos raramente dicen "click here". Usan textos descriptivos como "Ver mi pedido" o "Acceder a mi cuenta" |
| **Patron de ataque** | Los phishers necesitan que hagas clic. Usan frases genericas porque envian millones de emails identicos |

---

**5. Features TF-IDF (las 1,000 variables `tfidf_0` a `tfidf_999`)**

Ya explicado arriba. Resumen: capturan el "vocabulario del phishing" automaticamente.

**Palabras con mayor peso TF-IDF en phishing (segun investigaciones):**
- "click", "verify", "account", "suspended", "winner"
- "congratulations", "selected", "prize", "urgent", "immediate"
- "login", "password", "security", "update", "confirm"

---

##### Variables de IMPORTANCIA MEDIA

**6. `subject_sentiment` y `body_sentiment` - Analisis de Sentimiento**

| Aspecto | Explicacion |
|---------|-------------|
| **Que mide** | El "tono emocional" del asunto y cuerpo del email, en escala 0 a 1 (0=muy negativo, 0.5=neutral, 1=muy positivo) |
| **Por que es util** | Phishing usa emociones extremas: MIEDO ("tu cuenta sera cerrada") o EUFORIA ("ganaste $1,000,000") |
| **Emails legitimos** | Tienden a ser neutrales o ligeramente positivos. Tu banco no te amenaza ni te promete premios |

**Ejemplos:**
```
Sentimiento NEGATIVO (sospechoso):
  "ALERTA: Actividad sospechosa detectada. Su cuenta sera BLOQUEADA"

Sentimiento MUY POSITIVO (sospechoso):
  "FELICITACIONES! Has sido SELECCIONADO para ganar $50,000 USD!"

Sentimiento NEUTRAL (normal):
  "Su estado de cuenta de enero esta disponible para consulta"
```

---

**7. `special_chars_ratio` - Ratio de Caracteres Especiales**

| Aspecto | Explicacion |
|---------|-------------|
| **Que mide** | Proporcion de caracteres especiales (!@#$%^&*) vs caracteres totales |
| **Por que es util** | Phishers usan caracteres especiales para: (1) evadir filtros de spam, (2) crear urgencia visual, (3) ofuscar URLs |
| **Ejemplo** | "URGENT!!! ACT NOW!!!" vs "Please review your statement" |

---

##### Variables de IMPORTANCIA BAJA (pero utiles como complemento)

**8. `subject_length`, `body_length`, `subject_words`, `body_words`**

| Aspecto | Explicacion |
|---------|-------------|
| **Que miden** | Longitud del asunto/cuerpo en caracteres y palabras |
| **Por que son utiles** | Phishing tiende a ser: (1) muy corto (solo un enlace) o (2) muy largo (para parecer oficial). Emails normales estan en el medio |
| **Limitacion** | Por si solos no distinguen bien. Un email corto legitimo y uno de phishing pueden tener la misma longitud |

---

#### Resumen de Importancia - Phishing

| Prioridad | Variable | Por que es importante |
|-----------|----------|----------------------|
| CRITICA | `url_count`, `urls` | 75% de phishing tiene URLs maliciosas - es el vector de ataque |
| CRITICA | `has_urgent` | Presion psicologica hace que victimas no piensen |
| CRITICA | `sender_domain_encoded` | 90%+ de ataques usan dominios falsificados |
| ALTA | `has_click` | Frase generica tipica de emails masivos maliciosos |
| ALTA | TF-IDF features | Captura vocabulario predecible del phishing |
| MEDIA | Sentiment | Emociones extremas (miedo/euforia) son sospechosas |
| MEDIA | `special_chars_ratio` | Exceso de !!! y simbolos indica spam/phishing |
| BAJA | Longitudes | Complementa pero no discrimina por si solo |

**Fuentes**: [MDPI Applied Sciences](https://www.mdpi.com/2076-3417/15/6/3396), [Nature Scientific Reports](https://www.nature.com/articles/s41598-025-20668-5), [PMC Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC11013960/), [Cofense](https://cofense.com/knowledge-center/10-most-common-signs-of-a-phishing-email)

---

### 6.2 Account Takeover (ATO) Detection - Explicacion Detallada

#### Contexto: ¿Que es Account Takeover?

Account Takeover (ATO) o "Toma de Control de Cuenta" ocurre cuando un atacante obtiene acceso a la cuenta de un usuario legitimo. A diferencia de brute force (adivinar contraseñas), en ATO el atacante **ya tiene las credenciales** (las compro en la dark web, las obtuvo por phishing, o las encontro en una filtracion de datos).

El desafio es: **¿Como distinguir al atacante del usuario real si ambos tienen la contraseña correcta?**

La respuesta es: **analizar el COMPORTAMIENTO**, no solo las credenciales.

#### Estadisticas del Problema

| Estadistica | Valor | Fuente |
|-------------|-------|--------|
| Incremento de ataques ATO año tras año | 354% | Sift Q3 2023 |
| Usuarios que han sufrido ATO | 18% | Sift Research |
| Tasa de exito en sector educacion | 88% | Industry Report |
| Tasa de exito en servicios financieros | 47% | Industry Report |

---

#### Explicacion Detallada de Cada Variable de ATO

##### Variables de IMPORTANCIA CRITICA

**1. `country_changed` - Cambio de Pais**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que mide** | Si el pais desde donde se hace login es diferente al pais del login anterior del mismo usuario |
| **Por que es CRITICA** | **98.6% de los ATOs en nuestro dataset tienen cambio de pais**. Esta es la variable mas poderosa |
| **Razon tecnica** | Los atacantes estan fisicamente en otro pais (generalmente Rusia, China, Nigeria, Brasil). Aunque usen VPN para ocultar su IP, es dificil simular la ubicacion exacta de la victima |
| **Ejemplo** | Usuario siempre se conecta desde Peru. De repente hay un login desde Ucrania → MUY sospechoso |

**¿Por que los atacantes no pueden falsificar la ubicacion facilmente?**

1. Necesitarian saber EXACTAMENTE donde vive cada victima
2. Tendrian que usar VPNs/proxies del pais correcto para cada victima individual
3. Los ataques son masivos (miles de cuentas), no pueden personalizar cada uno

---

**2. `ip_changed` - Cambio de Direccion IP**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que mide** | Si la direccion IP del login actual es diferente a la del login anterior |
| **Que es una IP** | Es como la "direccion de casa" de tu conexion a internet. Cada vez que te conectas, tu proveedor (Movistar, Claro, etc.) te asigna una IP |
| **Por que es importante** | Usuarios normales tienden a conectarse desde pocas IPs (casa, trabajo, celular). Un cambio repentino de IP + otros factores = sospechoso |
| **Limitacion** | Por si sola no es suficiente. Usuarios legitimos cambian de IP (viajan, usan datos moviles, etc.) |

**Combinacion poderosa:**
```
ip_changed=1 + country_changed=1 + is_rapid_login=1 = MUY PROBABLE ATO
ip_changed=1 + country_changed=0 + is_rapid_login=0 = Probablemente legitimo (cambio de red normal)
```

---

**3. `is_suspicious_ip` - IP Sospechosa**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que mide** | Si la IP desde donde se conecta es usada por muchos usuarios diferentes (mas de 10) |
| **Por que es critica** | IPs compartidas por muchos usuarios indican: VPNs publicas, proxies anonimos, redes Tor, o botnets |
| **Como atacan** | Atacantes usan servicios de anonimizacion para ocultar su ubicacion real. Estas IPs son usadas por miles de personas |
| **Dato tecnico** | Si una IP tiene 500 usuarios diferentes, es casi seguro que es un proxy/VPN, no una conexion residencial normal |

**Tipos de IPs sospechosas:**
- VPNs comerciales (NordVPN, ExpressVPN, etc.)
- Red Tor (anonimato extremo)
- Proxies publicos
- IPs de datacenters/hosting (AWS, Google Cloud, etc.)
- IPs en listas negras de seguridad

---

##### Variables de IMPORTANCIA ALTA

**4. `is_night` e `is_business_hours` - Patron Temporal**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que miden** | `is_night`: si el login es entre 22:00 y 06:00. `is_business_hours`: si es entre 09:00 y 17:00 |
| **Por que son importantes** | Cada usuario tiene un patron de horarios. Si siempre te conectas de dia y de repente hay un login a las 3am, es sospechoso |
| **Razon del atacante** | Los atacantes estan en OTRAS zonas horarias. Cuando es de noche para ti, puede ser horario laboral para ellos |
| **Ejemplo** | Usuario en Peru (GMT-5) siempre se conecta 9am-6pm. Login a las 3am Peru = 11am en Moscu → posible atacante ruso |

---

**5. `browser_changed` y `device_changed` - Cambio de Navegador/Dispositivo**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que miden** | Si el navegador (Chrome, Firefox, Safari) o tipo de dispositivo (PC, celular, tablet) cambio |
| **Por que son importantes** | Los usuarios son criaturas de habito. Usan el mismo navegador y dispositivo consistentemente |
| **Contexto** | Cambio de dispositivo SOLO no es sospechoso (compraste telefono nuevo). Cambio de dispositivo + pais + IP + horario raro = MUY sospechoso |

**Ejemplo de fingerprinting:**
```
Usuario normal:
  - Siempre: Chrome 120, Windows 11, PC

Login sospechoso:
  - Firefox 115, Linux, PC  ← Todo cambio de repente
```

---

**6. `time_since_last_login_hours` e `is_rapid_login` - Tiempo Entre Logins**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que miden** | Cuantas horas pasaron desde el ultimo login, y si fue menos de 1 hora |
| **Concepto clave: "Viaje Imposible"** | Si un usuario se conecta desde Lima a las 10:00am y luego desde Tokyo a las 10:30am, es FISICAMENTE IMPOSIBLE haber viajado. El vuelo Lima-Tokyo toma 20+ horas |
| **Por que es critico** | Este patron es una **firma definitiva** de ATO. No hay explicacion legitima |

**Calculo de viaje imposible:**
```
Login 1: Lima, Peru - 10:00 AM
Login 2: Tokyo, Japon - 10:30 AM (30 minutos despues)

Distancia Lima-Tokyo: ~15,500 km
Tiempo minimo de vuelo: ~20 horas

30 minutos < 20 horas → IMPOSIBLE → ATO CONFIRMADO
```

---

##### Variables de IMPORTANCIA MEDIA

**7. `rtt_zscore` e `is_abnormal_rtt` - Latencia de Red**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que es RTT** | "Round-Trip Time" = tiempo que tarda un paquete de datos en ir al servidor y volver. Se mide en milisegundos (ms) |
| **Que es Z-score** | Medida estadistica de "que tan lejos del promedio" esta un valor. Z-score > 2 significa "muy anormal" |
| **Por que es util** | Conexiones a traves de VPNs/proxies tienen latencia MAS ALTA que conexiones directas (los datos viajan mas lejos) |
| **Ejemplo** | Usuario normalmente tiene RTT de 50ms (conexion local). De repente tiene RTT de 500ms → probablemente esta usando VPN/proxy |

**Ilustracion de RTT:**
```
Conexion DIRECTA (usuario real):
  PC → Router casa → ISP → Servidor banco
  RTT: 30-100ms (tipico)

Conexion via VPN (posible atacante):
  PC atacante → VPN en otro pais → ISP del VPN → Servidor banco
  RTT: 200-800ms (mucho mas alto)
```

---

**8. `country_count_per_user` - Cantidad de Paises Historicos**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que mide** | Cuantos paises diferentes ha usado este usuario historicamente |
| **Por que es util** | Ayuda a contextualizar. Un usuario que SIEMPRE se conecta desde Peru y de repente desde Rusia es muy diferente a un usuario que viaja frecuentemente (ejecutivo, consultor) |
| **Uso en modelo** | Si `country_count_per_user` = 1 y `country_changed` = 1 → MUY sospechoso. Si `country_count_per_user` = 10 y `country_changed` = 1 → menos sospechoso |

---

##### Variables de IMPORTANCIA BAJA

**9. `os_changed` - Cambio de Sistema Operativo**

| Aspecto | Explicacion |
|---------|-------------|
| **Que mide** | Si el sistema operativo (Windows, Mac, Linux, iOS, Android) cambio |
| **Por que es BAJA prioridad** | Muchos usuarios legitimos usan multiples SO (laptop Windows en trabajo, iPhone personal, iPad en casa) |
| **Cuando es util** | Solo como factor complementario cuando otros indicadores ya son sospechosos |

---

#### El Concepto Clave: Risk-Based Authentication (RBA)

Nuestro modelo implementa **RBA** (Autenticacion Basada en Riesgo), que es el estandar de la industria:

```
                    ┌─────────────────────────────┐
                    │      Usuario intenta        │
                    │          login              │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │   Analizar factores de      │
                    │   riesgo (35 variables)     │
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
      ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
      │  RIESGO BAJO  │   │ RIESGO MEDIO  │   │  RIESGO ALTO  │
      │ (mismo lugar, │   │ (nuevo disp.) │   │ (otro pais,   │
      │  mismo disp.) │   │               │   │  IP sospech.) │
      └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
              │                   │                   │
      ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
      │    ACCESO     │   │   VERIFICAR   │   │    BLOQUEAR   │
      │   PERMITIDO   │   │  (2FA, email) │   │   Y ALERTAR   │
      └───────────────┘   └───────────────┘   └───────────────┘
```

---

#### ¿Por que el F1-Score es "Solo" 75.86%?

Nuestro modelo tiene F1-Score de 75.86%, que parece bajo comparado con Phishing (99%) o Brute Force (99.97%). Esto se debe al **desbalance extremo** del dataset:

| Clase | Porcentaje | Cantidad |
|-------|------------|----------|
| Normal | 99.83% | 84,996 registros |
| ATO | 0.17% | 145 registros |

**Explicacion:**

Si el modelo simplemente dijera "todo es normal", tendria 99.83% de accuracy pero 0% de deteccion de ATO. Nuestro modelo detecta **78.57% de los ATOs reales** (recall) con **73.33% de precision** (cuando dice ATO, acierta 73% de las veces).

En contexto de seguridad, esto es **aceptable** porque:
- Es mejor tener falsos positivos (verificar usuarios legitimos) que falsos negativos (dejar pasar atacantes)
- El ROC-AUC de 98.06% indica excelente capacidad de separacion

**Fuentes**: [Transmit Security](https://transmitsecurity.com/blog/detecting-user-anomalies-and-account-takeovers-with-advanced-machine-learning), [SEON](https://seon.io/resources/account-takeover-fraud/), [ACM Research](https://dl.acm.org/doi/10.1145/3546069), [RBA Research](https://riskbasedauthentication.org/)

---

### 6.3 Brute Force Detection - Explicacion Detallada

#### Contexto: ¿Que es un Ataque de Fuerza Bruta?

Un ataque de fuerza bruta es cuando un atacante intenta **adivinar contraseñas** probando miles o millones de combinaciones automaticamente. A diferencia de ATO (donde ya tienen la contraseña), aqui estan intentando descubrirla.

**Tipos de ataques de fuerza bruta:**
- **Brute Force puro**: Probar todas las combinaciones (a, b, c... aa, ab, ac... aaa, aab...)
- **Diccionario**: Probar palabras comunes (password, 123456, admin, qwerty...)
- **Credential stuffing**: Probar contraseñas filtradas de otros sitios
- **Spray**: Probar pocas contraseñas comunes en MUCHAS cuentas

#### ¿Que es un "Flujo de Red" (Network Flow)?

Para entender las variables de Brute Force, primero hay que entender que es un "flujo de red":

**Un flujo de red es una "conversacion" entre dos computadoras:**

```
Tu PC (Cliente)                          Servidor del Banco
     │                                          │
     │───── Paquete 1: "Hola, quiero login" ────▶│
     │◀──── Paquete 2: "OK, dame usuario" ──────│
     │───── Paquete 3: "Usuario: juan123" ──────▶│
     │◀──── Paquete 4: "OK, dame password" ─────│
     │───── Paquete 5: "Password: ****" ────────▶│
     │◀──── Paquete 6: "Incorrecto, intenta" ───│
     │                                          │
     └──────────── ESTO ES UN FLUJO ────────────┘
```

Cada flujo tiene caracteristicas medibles: cuantos paquetes, cuantos bytes, cuanto tiempo duro, etc.

---

#### El Concepto de "Trafico Plano" (Flat Traffic)

Los ataques de fuerza bruta generan un patron MUY distintivo llamado **"trafico plano"**:

**Trafico HUMANO (normal):**
```
Intento 1: 500ms de duracion, 8 paquetes
  (humano escribe usuario y password)
Intento 2: 3 segundos despues, 450ms duracion, 7 paquetes
  (humano piensa "¿cual era mi password?")
Intento 3: 45 segundos despues, 600ms duracion, 9 paquetes
  (humano revisa su cuaderno de passwords)
```

**Trafico de BOT (ataque):**
```
Intento 1: 50ms de duracion, 6 paquetes
Intento 2: 50ms de duracion, 6 paquetes  ← 10ms despues
Intento 3: 50ms de duracion, 6 paquetes  ← 10ms despues
Intento 4: 50ms de duracion, 6 paquetes  ← 10ms despues
... (miles de intentos identicos)
```

**Caracteristicas del trafico plano:**
- Duracion IDENTICA en cada intento
- Cantidad de paquetes IDENTICA
- Tamaño de paquetes IDENTICO
- Tiempo entre intentos MINIMO y CONSTANTE

Esto es IMPOSIBLE para un humano, pero trivial para un script automatizado.

---

#### Explicacion Detallada de Cada Variable de Brute Force

##### Variables de IMPORTANCIA CRITICA

**1. `Bwd Pkts/s` - Paquetes por Segundo hacia Atras (Backward)**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que mide** | Cuantos paquetes POR SEGUNDO envia el SERVIDOR de vuelta al cliente |
| **Que es "backward"** | "Hacia atras" = del servidor hacia el cliente. El servidor responde a cada intento de login |
| **Por que es CRITICA** | En ataques, el servidor responde a VELOCIDAD EXTREMA porque recibe miles de intentos por segundo. **En nuestro dataset, ataques tienen 112.7x mas Bwd Pkts/s que trafico normal** |
| **Numero real** | Trafico normal: ~5 paquetes/segundo. Ataque: ~500+ paquetes/segundo |

**Visualizacion:**
```
NORMAL (humano):
  Servidor envia: █ (pausa) █ (pausa larga) █
  Bwd Pkts/s: 2-5

ATAQUE (bot):
  Servidor envia: █████████████████████████████████████
  Bwd Pkts/s: 500+
```

---

**2. `Flow Pkts/s` - Paquetes por Segundo Totales en el Flujo**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que mide** | Total de paquetes (ida + vuelta) dividido por duracion del flujo |
| **Por que es CRITICA** | Combina la velocidad del atacante Y la velocidad de respuesta del servidor. **24.7x mas alto en ataques** |
| **Interpretacion** | Flujos con >100 paquetes/segundo son casi seguro automatizados. Humanos no pueden generar esa tasa |

---

**3. `Flow Duration` - Duracion del Flujo**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que mide** | Tiempo total desde el primer paquete hasta el ultimo, en microsegundos |
| **Por que es CRITICA** | Ataques tienen flujos **100x MAS CORTOS** que trafico normal |
| **Razon** | Los bots no esperan. Envian credenciales, reciben "incorrecto", e inmediatamente pasan al siguiente intento |
| **Numero real** | Intento humano: 2-10 segundos. Intento de bot: 50-200 milisegundos |

**Por que la duracion corta indica ataque:**
```
HUMANO:
  1. Abre pagina (500ms)
  2. Lee el formulario (1 segundo)
  3. Escribe usuario (2 segundos)
  4. Escribe password (3 segundos)
  5. Hace clic en "Login" (500ms)
  6. Espera respuesta (1 segundo)
  TOTAL: ~8 segundos = 8,000,000 microsegundos

BOT:
  1. Envia POST /login con credenciales (10ms)
  2. Recibe respuesta "401 Unauthorized" (20ms)
  3. Cierra conexion (5ms)
  TOTAL: ~35ms = 35,000 microsegundos

8,000,000 / 35,000 = 228x mas largo el humano
```

---

##### Variables de IMPORTANCIA ALTA

**4. `PSH Flag Cnt` - Conteo de Flags PSH**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que es PSH** | "Push" es un flag (bandera) del protocolo TCP. Cuando esta activado, dice "enviar estos datos INMEDIATAMENTE, no esperar a llenar el buffer" |
| **Por que indica ataque** | Herramientas de hacking usan PSH para enviar datos lo mas rapido posible. **1.96x mas alto en ataques** |
| **Contexto tecnico** | Software normal (navegadores) optimizan el uso de red y no siempre usan PSH. Scripts de ataque priorizan velocidad |

---

**5. `Fwd Pkt Len Mean` y `Fwd Pkt Len Std` - Tamaño Promedio y Desviacion de Paquetes Forward**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que miden** | El tamaño promedio de los paquetes que el CLIENTE envia, y que tan variable es ese tamaño |
| **Que es "forward"** | "Hacia adelante" = del cliente hacia el servidor (los intentos de login) |
| **Por que indica ataque** | En ataques, TODOS los paquetes tienen tamaño casi identico porque son el mismo comando repetido (solo cambia la password). Std (desviacion estandar) muy BAJA = sospechoso |

**Visualizacion del concepto:**
```
HUMANO (tamaños variados):
  Paquete 1: 234 bytes (escribe "hola")
  Paquete 2: 567 bytes (escribe "como estan amigos")
  Paquete 3: 123 bytes (escribe "adios")
  Mean: 308 bytes, Std: 183 (ALTA variabilidad)

BOT (tamaños uniformes):
  Paquete 1: 145 bytes (login:admin, pass:password123)
  Paquete 2: 147 bytes (login:admin, pass:password124)
  Paquete 3: 146 bytes (login:admin, pass:password125)
  Mean: 146 bytes, Std: 0.8 (MUY BAJA variabilidad) ← SOSPECHOSO
```

---

**6. `Flow IAT Mean` - Inter-Arrival Time Promedio**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que es IAT** | "Inter-Arrival Time" = tiempo entre la llegada de un paquete y el siguiente |
| **Que mide Flow IAT Mean** | El promedio de tiempo entre paquetes consecutivos en el flujo |
| **Por que indica ataque** | Humanos tienen IAT VARIABLE (piensan, escriben, dudan). Bots tienen IAT muy BAJO y CONSTANTE |
| **Numero tipico** | Humano: IAT promedio 500-2000ms. Bot: IAT promedio 5-50ms |

**Visualizacion:**
```
HUMANO:
  Paquete 1 ──── 1200ms ──── Paquete 2 ──── 800ms ──── Paquete 3
  IAT Mean: 1000ms, IAT Std: 283ms (variabilidad humana)

BOT:
  Paquete 1 ── 15ms ── Paquete 2 ── 14ms ── Paquete 3 ── 16ms ── Paquete 4
  IAT Mean: 15ms, IAT Std: 0.8ms (precision de maquina) ← SOSPECHOSO
```

---

##### Variables de IMPORTANCIA MEDIA

**7. `RST Flag Cnt` - Conteo de Flags RST**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que es RST** | "Reset" es un flag TCP que indica "cerrar esta conexion inmediatamente" |
| **Por que indica ataque** | Cuando el servidor rechaza un intento de login, puede enviar RST para cerrar la conexion rapidamente. Muchos RST = muchos rechazos = probable ataque |
| **Contexto** | Un flujo normal tiene 0-1 RST. Un flujo de ataque puede tener docenas |

---

**8. `Dst Port` - Puerto de Destino**

| Aspecto | Explicacion Detallada |
|---------|----------------------|
| **Que es un puerto** | Es como un "numero de apartamento" en una direccion. La IP es el edificio, el puerto es el apartamento especifico |
| **Puertos comunes atacados** | 22 (SSH), 21 (FTP), 3389 (RDP), 80/443 (Web), 3306 (MySQL) |
| **Por que es util** | Ayuda a identificar QUE servicio esta siendo atacado. Ataques a puerto 22 = brute force SSH |

**Puertos y servicios:**
```
Puerto 21  → FTP (transferencia de archivos)
Puerto 22  → SSH (terminal remota) ← MUY atacado
Puerto 23  → Telnet (terminal antigua, insegura)
Puerto 80  → HTTP (web sin cifrar)
Puerto 443 → HTTPS (web cifrada)
Puerto 3306 → MySQL (base de datos)
Puerto 3389 → RDP (escritorio remoto Windows) ← MUY atacado
```

---

##### Variables de IMPORTANCIA BAJA (contextuales)

**9. `Active Mean`, `Idle Mean` - Tiempos de Actividad e Inactividad**

| Aspecto | Explicacion |
|---------|-------------|
| **Que miden** | Periodos donde hay transmision activa vs periodos de silencio |
| **Por que son utiles** | Ataques tienen muy poco tiempo idle (inactivo). Trafico normal tiene pausas |
| **Limitacion** | Menos discriminantes que las variables de velocidad |

---

**10. `Tot Fwd Pkts`, `Tot Bwd Pkts` - Total de Paquetes**

| Aspecto | Explicacion |
|---------|-------------|
| **Que miden** | Cantidad total de paquetes en cada direccion |
| **Por que son utiles** | Flujos de ataque pueden tener MUCHOS paquetes (miles de intentos) o POCOS (intentos rapidos individuales) |
| **Depende de la fase** | Fase de escaneo = pocos paquetes. Fase de brute force = muchos paquetes |

---

#### Fases de un Ataque de Fuerza Bruta

Los investigadores identifican 3 fases distintas:

```
┌─────────────────────────────────────────────────────────────────┐
│                    LINEA DE TIEMPO DEL ATAQUE                   │
├─────────────────┬─────────────────────────┬─────────────────────┤
│   FASE 1:       │      FASE 2:            │    FASE 3:          │
│   ESCANEO       │    BRUTE FORCE          │   COMPROMISO        │
├─────────────────┼─────────────────────────┼─────────────────────┤
│ - Buscar        │ - Miles de intentos     │ - Acceso exitoso    │
│   puertos       │ - Trafico PLANO         │ - Descarga datos    │
│   abiertos      │ - Duracion CORTA        │ - Instala backdoor  │
│ - Pocos         │ - Paquetes/s MUY ALTO   │ - Patron DIFERENTE  │
│   paquetes      │ - IAT muy bajo          │   a fases previas   │
│ - Muchos        │ - Objetivo especifico   │                     │
│   destinos      │                         │                     │
├─────────────────┼─────────────────────────┼─────────────────────┤
│ Tot Fwd Pkts:   │ Tot Fwd Pkts: ALTO      │ Cambio de patron    │
│ BAJO            │ Flow Pkts/s: MUY ALTO   │ indica exito del    │
│ Muchas IPs      │ Flow Duration: MUY BAJO │ atacante            │
│ destino         │ PSH Flag: ALTO          │                     │
└─────────────────┴─────────────────────────┴─────────────────────┘
```

---

#### ¿Por que Random Forest Funciona tan Bien?

Nuestro modelo usa Random Forest y logra **99.97% F1-Score**. Esto es casi perfecto. ¿Por que?

1. **Trafico de ataque es MUY distintivo**: Las diferencias entre humano y bot son enormes (100x en duracion, 112x en paquetes/segundo)

2. **Pocas features son suficientes**: Estudios muestran que solo 8-10 features logran >99% accuracy. Nosotros usamos 60 para ser exhaustivos

3. **Dataset balanceado**: A diferencia de ATO (0.17% positivo), Brute Force tiene 50/50, lo que facilita el entrenamiento

4. **Random Forest maneja bien outliers**: Al promediar muchos arboles de decision, no se confunde con casos raros

**Fuentes**: [Springer Journal](https://link.springer.com/article/10.1007/s10922-017-9421-4), [CSE-CIC-IDS2018 Survey](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-020-00382-x), [IEEE Research](https://ieeexplore.ieee.org/document/7033609/), [ArXiv Analysis](https://arxiv.org/abs/2307.11544)

---

### 6.4 Resumen Ejecutivo: ¿Que Variables Priorizar?

#### Tabla Resumen de Importancia

| Modelo | Variables CRITICAS | Variables ALTAS | Variables MEDIAS |
|--------|-------------------|-----------------|------------------|
| **Phishing** | `url_count` (75% de phishing tiene URLs), `has_urgent` (presion psicologica), `sender_domain_encoded` (90%+ spoofing) | TF-IDF features (vocabulario predecible), `has_click` (frases genericas) | Sentiment (emociones extremas), `special_chars_ratio` |
| **ATO** | `country_changed` (98.6% de ATOs!), `ip_changed`, `is_suspicious_ip` (VPNs/proxies) | `is_night`/`is_business_hours` (patron temporal), `is_rapid_login` (viaje imposible) | `rtt_zscore` (latencia anormal), `country_count_per_user` |
| **Brute Force** | `Bwd Pkts/s` (112x mas alto), `Flow Duration` (100x mas corto), `Flow Pkts/s` (24x mas alto) | `PSH Flag Cnt` (firma de herramientas), `Flow IAT Mean` (velocidad sobrehumana), `Fwd Pkt Len Std` (uniformidad) | `RST Flag Cnt`, `Dst Port` |

#### Recomendaciones para Ajuste de Hiperparametros

**Phishing:**
- Considerar aumentar peso de `url_count` y `has_urgent` en el modelo
- TF-IDF: experimentar con `ngram_range=(1,3)` para capturar frases completas

**ATO:**
- Usar class_weight para compensar el desbalance extremo (0.17% vs 99.83%)
- Considerar threshold mas bajo (0.3-0.4) para mejorar recall
- Priorizar `country_changed` como feature principal

**Brute Force:**
- Modelo ya es excelente (99.97%). Considerar reducir features de 60 a 10-15 mas importantes para eficiencia
- Features prioritarias: `Bwd Pkts/s`, `Flow Duration`, `Flow Pkts/s`, `PSH Flag Cnt`

---

**Documento generado:** 2026-01-29
**Proyecto:** Sistema de Prediccion de Incidentes de Ciberseguridad
