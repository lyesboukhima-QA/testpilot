// Fichier de support global — chargé avant chaque spec
// Importer les commandes personnalisées
import './commands'

// Ignorer les erreurs JS non-critiques de l'app testée
Cypress.on('uncaught:exception', (err) => {
  // Retourner false empêche Cypress de faire échouer le test
  if (err.message.includes('ResizeObserver loop')) return false
})
