# Alvioli Dependency Migration Guide

This document outlines the changes made to update Alvioli's dependencies and resolve deprecation warnings.

## Major Updates

### 1. ESLint v8 → v9
- **Breaking Change**: New flat config system
- **Action**: Created new `eslint.config.js` with flat config format
- **Removed**: Old `.eslintrc.*` files are no longer supported

### 2. Puppeteer v21 → v23
- **Security**: Fixes multiple security vulnerabilities
- **Performance**: Improved browser automation performance
- **Compatibility**: Better Chrome/Chromium compatibility

### 3. Chalk v4 → v5
- **Breaking Change**: Now ESM-only
- **Action**: Updated TypeScript config to handle ESM modules
- **Benefit**: Better tree-shaking and smaller bundle size

### 4. Commander v11 → v12
- **Improvements**: Better TypeScript support
- **New Features**: Enhanced argument parsing

### 5. Inquirer v8 → v12
- **Breaking Changes**: API improvements
- **Better Types**: Enhanced TypeScript definitions
- **Performance**: Faster prompt rendering

### 6. Node.js Requirement: v16+ → v18+
- **Reason**: Newer packages require Node.js 18+
- **Benefit**: Access to latest Node.js features and security updates

## Configuration Changes

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Node"
  }
}
```

### Package.json Updates
- Added `"type": "module"` for ESM support
- Updated all dependency versions
- New scripts for better development experience

### ESLint Configuration
- Migrated to flat config (`eslint.config.js`)
- Updated rules for TypeScript
- Better integration with modern tooling

## Resolved Deprecation Warnings

✅ **inflight@1.0.6** - Removed (was a transitive dependency)
✅ **@humanwhocodes/config-array** - Updated to @eslint/config-array
✅ **rimraf@3.0.2** - Updated to v5+
✅ **glob@7.2.3** - Updated to v10+
✅ **@humanwhocodes/object-schema** - Updated to @eslint/object-schema
✅ **gauge@4.0.4** - Removed (was a transitive dependency)
✅ **are-we-there-yet@3.0.1** - Removed (was a transitive dependency)
✅ **eslint@8.57.1** - Updated to v9.12.0
✅ **@npmcli/move-file** - Updated to @npmcli/fs
✅ **npmlog@6.0.2** - Removed (was a transitive dependency)
✅ **puppeteer@21.11.0** - Updated to v23.5.0

## Migration Steps

1. **Clean Install**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Update Scripts**:
   ```bash
   npm run update-deps  # Runs the automated update script
   ```

3. **Verify Build**:
   ```bash
   npm run build
   npm run lint
   npm test
   ```

4. **Test Application**:
   ```bash
   npm run dev alido test command
   ```

## Breaking Changes to Watch

### Chalk v5
- Now requires ESM imports
- No more CommonJS support
- May affect custom color functions

### ESLint v9
- Flat config only
- Some rules may have changed
- Plugin compatibility may vary

### Inquirer v12
- API changes in prompt types
- Better async/await support
- Some legacy options removed

## Benefits

- 🔒 **Security**: All known vulnerabilities resolved
- 🚀 **Performance**: Faster builds and runtime performance
- 🛠️ **Developer Experience**: Better TypeScript support and tooling
- 📦 **Bundle Size**: Smaller production bundles with ESM
- 🔧 **Maintenance**: Up-to-date with latest ecosystem standards

## Troubleshooting

### If you encounter module resolution errors:
```bash
# Clear TypeScript cache
npx tsc --build --clean

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### If ESLint fails:
```bash
# Check config syntax
npx eslint --print-config src/cli.ts

# Fix auto-fixable issues
npm run lint:fix
```

### If build fails:
```bash
# Check TypeScript errors
npx tsc --noEmit

# Clean and rebuild
npm run clean
npm run build
```

## Next Steps

After migration, you can:
1. Continue with the next implementation tasks
2. Take advantage of new features in updated packages
3. Enjoy improved development experience with better tooling

For any issues, check the individual package documentation or create an issue in the project repository.