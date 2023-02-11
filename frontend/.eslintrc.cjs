/* eslint-disable no-undef */
/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')
customRules = require('./eslintrules.js')

module.exports = {
  root: true,
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-prettier',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
  },
  ignorePatterns: ['**/icons/*.vue'],
  rules: { ...customRules },
}
