
```bash
pipenv shell

python main.py
```

Antes de ejecutar la solución, instalar todas las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

Si necesitas reindexar la base de conocimientos, puedes hacerlo ejecutando el script `indexer.py` que se encuentra en el mismo directorio:

```bash
python indexer.py
```

Este script generará un directorio `index` que contiene la base de datos de vectores FAISS. Esto es útil si has realizado cambios en la base de conocimientos y necesitas actualizar los índices para reflejar esos cambios.
