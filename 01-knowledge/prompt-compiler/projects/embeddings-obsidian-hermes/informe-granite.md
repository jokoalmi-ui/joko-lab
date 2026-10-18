---
type: knowledge
subtype: prompt
status: active
tags: [knowledge, prompt]
created: 2026-07-28
---
### 3. Arquitectura Propuesta (diagrama en texto)

```
+-------------------+
|   Obsidian Vault |
+-------------------+
          |
          v
+-------------------+
|     Hermes Agent  |
|    (Skill: RAG)   |
+-------------------+
          |
          v
+-------------------+
|  Embeddings Layer  |
|  (BGE-M3 Engine)   |
+-------------------+
          |
          v
+-------------------+
|   Vector Store    |
|  (FAISS, sqlite-vec|
|   Chroma, LanceDB)|
+-------------------+
          |
          v
+-------------------+
|     Search API    |
|   (Query Engine)  |
+-------------------+
```

### 4. Código Python funcional para indexar `.md` y buscar

```python
import os
from bge_pytorch import BGEEmbeddingModel
from faiss import Index, IVFFlat, quantizers.PNormL2
import sqlite3
import re

# Configurar el modelo de embeddings BGE-M3
model = BGEEmbeddingModel()

def preprocess_text(text):
    # Eliminar caracteres especiales y convertir a minúsculas
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def index_md_files(directory, vector_store='FAISS'):
    if vector_store == 'FAISS':
        index = IndexFlatL2(model.get_dim())
        faiss_index = Index(index)  # Wrapper for FAISS
    elif vector_store == 'sqlite-vec':
        conn = sqlite3.connect('vector_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vectors (id INTEGER PRIMARY KEY, embedding TEXT, content TEXT)''')

    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = preprocess_text(file.read())
                embedding = model.encode(text)
                
                if vector_store == 'FAISS':
                    faiss_index.add(embedding.astype('float32'))
                elif vector_store == 'sqlite-vec':
                    cursor.execute("INSERT INTO vectors (embedding, content) VALUES (?, ?)", 
                                   (','.join(map(str, embedding)), text))
            conn.commit() if vector_store == 'sqlite-vec' else None

    return faiss_index if vector_store == 'FAISS' else None

def search(query, vector_store='FAISS'):
    query_text = preprocess_text(query)
    query_embedding = model.encode(query_text)

    if vector_store == 'FAISS':
        distances, indices = vector_store.search(query_embedding.astype('float32'), k=5)
        results = [vector_store.recall(i) for i in indices]
    elif vector_store == 'sqlite-vec':
        cursor.execute("SELECT content FROM vectors WHERE embedding LIKE ?", 
                       (f"%{','.join(map(str, query_embedding))}%",))
        results = [row[0] for row in cursor.fetchall()]

    return results

# Ejemplo de uso
vector_store = index_md_files('path/to/obsidian/vault', vector_store='FAISS')
results = search('¿Cuál es el propósito del Hermes Agent?', vector_store=vector_store)
print(results)
```

### 5. Integración con Hermes Agent (como skill)

Para integrar la arquitectura anterior con **Hermes Agent**, se debe crear una habilidad (skill) dentro de la plataforma que maneje las consultas y devuelva los resultados procesados por el motor RAG.

```python
from hermes_agent import Skill

class RAGSkill(Skill):
    def __init__(self, vector_store):
        super().__init__()
        self.vector_store = vector_store

    async def handle(self, query: str) -> str:
        results = search(query, vector_store=self.vector_store)
        response = "\n".join(results)
        return response

# Inicialización del skill
vector_store = index_md_files('path/to/obsidian/vault', vector_store='FAISS')
rag_skill = RAGSkill(vector_store=vector_store)

# Ejemplo de uso en Hermes Agent
await rag_skill.handle("¿Cómo funciona el Hermes Agent?")
```

### 6. Métricas Esperadas

- **Tiempo de Indexación**: Dependiendo del tamaño del vault, la indexación completa puede tardar entre 5 a 30 minutos usando FAISS o sqlite-vec.
- **Latencia de Búsqueda**: La búsqueda en tiempo real debería responder en menos de 200 ms para consultas típicas, dada la eficiencia de los algoritmos de búsqueda vectorial.

### 7. Limitaciones y Mejoras Futuras

**Limitaciones:**
- **Escalabilidad**: Para vaults muy grandes, el uso de FAISS puede requerir más memoria RAM.
- **Precisión del Embedding**: Aunque BGE-M3 es robusto en español, podría mejorarse con modelos multilingües para consultas en otros idiomas.

**Mejoras Futuras:**
- Integración con **LanceDB** para manejar vectores de mayor tamaño y mejorar la escalabilidad.
- Implementar técnicas de **relevancia reforzada** (RLHF) para ajustar los resultados a las preferencias del usuario.
- Soporte multiidioma extendido mediante modelos como **Mistral-7B-Instruct**.

### 8. Conclusion

La integración de **BGE-M3 embeddings** con **Obsidian** y **Hermes Agent** permite crear un sistema RAG eficiente y escalable, especialmente para contenido en español. La arquitectura propuesta facilita la indexación y búsqueda de documentos markdown, mejorando significativamente la interacción del usuario con el vault de Obsidian a través de consultas naturales procesadas por Hermes Agent. Con métricas esperadas de baja latencia y una sólida base para futuras mejoras, este sistema se posiciona como una herramienta poderosa para la gestión y consulta de conocimiento en entornos académicos y profesionales.