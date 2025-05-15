export default [
  {
    files: ["*.js"],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly",
        chrome: "readonly",
        // добавь сюда другие глобальные переменные, если используешь
      },
    },
    rules: {
      semi: ["error", "always"],
      quotes: ["error", "double"],
      "no-unused-vars": "warn",
    },
  },
];
