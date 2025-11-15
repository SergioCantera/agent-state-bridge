# Desarrollo local de agent-state-bridge

Para evitar errores de tipado y compilación durante el desarrollo del paquete, instala las dependencias necesarias en modo desarrollo:

```bash
npm install --save-dev react @types/react zustand @types/zustand react-markdown @types/react-markdown
```

Esto asegura que el editor y TypeScript encuentren los tipos y módulos requeridos.

- **dependencies**: Se instalarán automáticamente cuando alguien use el paquete.
- **peerDependencies**: El usuario debe tenerlas ya instaladas en su proyecto (npm/yarn avisará si faltan).
- **devDependencies**: Solo necesarias para desarrollo local del paquete.

## Notas
- Si usas un monorepo, puedes aprovechar los enlaces locales (ej: `npm link` o workspaces).
- Antes de publicar, ejecuta `npm run build` para compilar a `dist/`.

---
¿Dudas? Consulta el README o abre un issue.
