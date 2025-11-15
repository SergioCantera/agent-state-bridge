# Guía de Publicación en npm

## Pre-requisitos

- Cuenta en npm: https://www.npmjs.com/signup
- npm CLI instalado (viene con Node.js)

## Pasos para publicar

### 1. Verificar que el paquete compila correctamente

```bash
npm run build
```

- Asegúrate de que la carpeta `dist/` se genera sin errores.

### 2. Verificar el contenido del paquete

```bash
npm pack --dry-run
```

- Esto muestra qué archivos se incluirán en el paquete sin crear el archivo .tgz.
- Verifica que solo se incluyan los archivos necesarios (dist/, README, LICENSE, package.json).

### 3. Hacer login en npm

```bash
npm login
```

- Ingresa tu username, password y email.
- Si tienes 2FA habilitado, ingresa el código.

### 4. Publicar el paquete

```bash
npm publish --access public
```

- `--access public` es necesario para paquetes scoped o la primera publicación.
- Si todo va bien, tu paquete estará disponible en https://www.npmjs.com/package/agent-state-bridge

### 5. Verificar la publicación

- Ve a https://www.npmjs.com/package/agent-state-bridge
- Prueba instalarlo en un proyecto de prueba:

```bash
npm install agent-state-bridge
```

## Actualizaciones futuras

### 1. Actualizar la versión

```bash
npm version patch  # 0.1.0 -> 0.1.1
npm version minor  # 0.1.1 -> 0.2.0
npm version major  # 0.2.0 -> 1.0.0
```

### 2. Commitear y hacer push

```bash
git push && git push --tags
```

### 3. Publicar la nueva versión

```bash
npm publish
```

## Notas importantes

- El nombre del paquete debe ser único en npm.
- Una vez publicado, **no puedes eliminar versiones** (solo deprecarlas).
- Usa versionado semántico (semver): MAJOR.MINOR.PATCH
- Antes de publicar, revisa bien el README, ya que será la página principal del paquete.

## Troubleshooting

- **Error 403:** Verifica que estás logueado y que el nombre no está tomado.
- **Error 402:** El nombre puede estar reservado o en la lista de spam.
- **Missing README:** Asegúrate de que README.md existe en el root.

---

¡Listo para publicar! 🚀
