# TypeScript Configuration Additions

After creating your Next.js project, the `tsconfig.json` will be auto-generated.

**Optional Enhancement**: Add path aliases for cleaner imports.

## Add Path Aliases (Recommended)

Edit `frontend/tsconfig.json` and ensure these settings exist:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Note**: `create-next-app` may already configure this. Verify before making changes.

## Usage

With path aliases configured, you can use:

```typescript
// Instead of: import { Button } from '../../../components/Button'
import { Button } from '@/components/Button'

// Instead of: import { apiClient } from '../../lib/api'
import { apiClient } from '@/lib/api'
```

## Next.js Config Integration

Ensure your `next.config.ts` is aware of path aliases (usually auto-configured):

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'standalone',
  // Path aliases are automatically resolved from tsconfig.json
}

export default nextConfig
```
