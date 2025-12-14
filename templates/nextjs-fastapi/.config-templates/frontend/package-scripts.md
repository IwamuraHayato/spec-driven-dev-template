# Package.json Scripts to Add

After creating your Next.js project with `create-next-app`, add the following scripts to your `frontend/package.json`:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",

    // Add these scripts below:
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,md}\"",
    "type-check": "tsc --noEmit"
  }
}
```

## Recommended: Add combined check script

For CI/CD pipelines, add a combined check script:

```json
{
  "scripts": {
    "check": "npm run lint && npm run format:check && npm run type-check"
  }
}
```

## Usage

```bash
# Format code
npm run format

# Check formatting (CI)
npm run format:check

# Type check
npm run type-check

# Run all checks
npm run check
```
