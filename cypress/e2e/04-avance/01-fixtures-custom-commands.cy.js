// MODULE 4 — AVANCÉ : Fixtures et Commandes personnalisées
//
// Fixtures = fichiers de données de test (JSON, CSV...)
//   → équivalent des fichiers de données Robot Framework
//
// Custom Commands = tes propres commandes cy.xxx()
//   → équivalent des Keywords Robot Framework

describe('Module 4 : Fixtures', () => {

  it('charger un fichier fixture JSON', () => {
    // cypress/fixtures/utilisateur.json
    cy.fixture('utilisateur').then((user) => {
      expect(user.email).to.eq('lyes@test.com')
      expect(user.role).to.eq('admin')
    })
  })

  it('utiliser une fixture dans un test réseau', () => {
    // Charger la fixture ET mocker la réponse avec
    cy.fixture('utilisateur').then((user) => {
      cy.intercept('GET', '**/users/1', { body: user }).as('getUser')
    })
  })

  it('utiliser une fixture comme alias', () => {
    // Syntaxe alternative : charge la fixture en tant qu'alias
    cy.fixture('utilisateur').as('userData')

    cy.get('@userData').then((user) => {
      cy.log(`Utilisateur : ${user.prenom} ${user.nom}`)
    })
  })
})

// Les Custom Commands sont définies dans cypress/support/commands.js
// On peut les appeler ici directement

describe('Module 4 : Custom Commands', () => {

  it('utiliser cy.connexion() — commande personnalisée', () => {
    // cy.connexion() est définie dans support/commands.js
    // Elle encapsule la logique de login
    cy.connexion('lyes@test.com', 'motdepasse123')

    // Après la connexion, on vérifie qu'on est bien connecté
    cy.url().should('include', 'example.cypress.io')
  })

  it('utiliser cy.verifierApi() — commande personnalisée', () => {
    cy.verifierApi('https://jsonplaceholder.typicode.com/posts/1', {
      id: 1,
      userId: 1,
    })
  })
})
