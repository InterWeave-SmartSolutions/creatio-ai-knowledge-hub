module.exports = {
  // Basic formatting
  semi: true,
  singleQuote: true,
  quoteProps: 'as-needed',
  trailingComma: 'es5',
  tabWidth: 2,
  useTabs: false,
  
  // Line formatting
  printWidth: 100,
  endOfLine: 'lf',
  
  // Object and array formatting
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'avoid',
  
  // File specific overrides
  overrides: [
    {
      files: '*.json',
      options: {
        parser: 'json',
        printWidth: 120
      }
    },
    {
      files: '*.md',
      options: {
        parser: 'markdown',
        printWidth: 80,
        proseWrap: 'always'
      }
    },
    {
      files: '*.css',
      options: {
        parser: 'css',
        singleQuote: false
      }
    },
    {
      files: '*.html',
      options: {
        parser: 'html',
        printWidth: 120
      }
    },
    {
      files: '*.xml',
      options: {
        parser: 'xml',
        printWidth: 120,
        xmlSelfClosingSpace: true,
        xmlWhitespaceSensitivity: 'ignore'
      }
    }
  ]
};
