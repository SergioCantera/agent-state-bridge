# Publishing to PyPI

## Pre-requisitos

- Cuenta en PyPI: https://pypi.org/account/register/
- `build` y `twine` instalados: `pip install build twine`

## Pasos para publicar

### 1. Verificar el paquete

```bash
cd python/
python -m build
```

- Esto crea archivos en `dist/` (.tar.gz y .whl)

### 2. Verificar el contenido

```bash
tar -tzf dist/agent-state-bridge-0.1.0.tar.gz
```

- Asegúrate de que incluya todos los archivos necesarios

### 3. Subir a TestPyPI (opcional pero recomendado)

```bash
python -m twine upload --repository testpypi dist/*
```

- Username: `__token__`
- Password: tu token de TestPyPI

### 4. Probar desde TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ agent-state-bridge
```

### 5. Publicar en PyPI oficial

```bash
python -m twine upload dist/*
```

- Username: `__token__`
- Password: tu token de PyPI

### 6. Verificar

- https://pypi.org/project/agent-state-bridge/
- `pip install agent-state-bridge`

## Actualizaciones

### 1. Actualizar versión en pyproject.toml

```toml
version = "0.1.1"  # o 0.2.0, 1.0.0
```

### 2. Limpiar builds anteriores

```bash
rm -rf dist/ build/ *.egg-info
```

### 3. Rebuild y publicar

```bash
python -m build
python -m twine upload dist/*
```

## Tokens de API

- PyPI: https://pypi.org/manage/account/token/
- TestPyPI: https://test.pypi.org/manage/account/token/

## Troubleshooting

- **403 Forbidden**: Verifica tu token y que el nombre no esté tomado
- **400 Bad Request**: Revisa que todos los campos en pyproject.toml sean válidos
- **File already exists**: No puedes re-subir la misma versión, incrementa el número

---

¡Listo para publicar! 🚀
