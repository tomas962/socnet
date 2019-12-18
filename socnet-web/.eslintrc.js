module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-unused-vars': 0,
    'no-undef': 0,
    'no-extra-semi': 0,
    'no-redeclare': 0,
    'no-mixed-spaces-and-tabs': 0
  },
  parserOptions: {
    parser: 'babel-eslint'
  }
}
