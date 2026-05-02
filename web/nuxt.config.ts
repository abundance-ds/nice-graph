export default defineNuxtConfig({
  compatibilityDate: "2025-01-01",
  future: { compatibilityVersion: 4 },
  modules: ["@nuxtjs/tailwindcss"],
  css: ["@/assets/css/main.css"],

  runtimeConfig: {
    databasePath: "../nice.db",
    anthropicApiKey: "",
  },

  app: {
    head: {
      title: "NICE Appraisals",
      meta: [
        {
          name: "description",
          content:
            "826 NICE Technology Appraisals: structured knowledge graph, full-text corpus, and AI-queryable search across drugs, ICERs, methodological decisions, and clinical evidence.",
        },
      ],
      link: [
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Open+Sans:wght@400;500;600&display=swap",
        },
      ],
    },
  },
});
