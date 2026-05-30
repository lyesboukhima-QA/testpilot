// MODULE 3 — INTERCEPT : Mocker les appels réseau
//
// cy.intercept() est l'outil le plus puissant de Cypress pour les tests UI.
// Il permet de :
//   - Espionner les requêtes réseau
//   - Mocker les réponses (sans toucher au serveur)
//   - Attendre qu'une requête soit complète avant d'asserter

describe('Module 3 : cy.intercept() — Mock réseau', () => {

  it('espionner une requête (spy) et attendre sa réponse', () => {
    // 1. Déclarer l'intercept AVANT de visiter la page
    cy.intercept('GET', '**/todos*').as('getTodos')

    cy.visit('https://jsonplaceholder.typicode.com')

    // 2. Déclencher l'action qui provoque la requête
    //    (ici on l'appelle manuellement via cy.request pour la démo)
    cy.request('https://jsonplaceholder.typicode.com/todos/1')

    // 3. cy.wait('@alias') attend que la requête arrive
    //    Puis on peut inspecter request et response
    // cy.wait('@getTodos').then(({ request, response }) => {
    //   expect(response.statusCode).to.eq(200)
    // })
  })

  it('mocker une réponse réseau (stub)', () => {
    // Remplace la vraie réponse API par une réponse fictive
    cy.intercept('GET', '**/posts/1', {
      statusCode: 200,
      body: {
        id: 1,
        title: 'Réponse mockée par Cypress',
        body: 'Ceci ne vient pas du serveur',
        userId: 99,
      },
    }).as('getPost')

    // cy.request utilise aussi l'intercept
    cy.request('https://jsonplaceholder.typicode.com/posts/1').then((response) => {
      // NOTE : cy.request() bypasse les intercepts dans certaines versions
      // L'intercept est surtout efficace pour les requêtes faites par le navigateur
    })
  })

  it('simuler une erreur réseau', () => {
    cy.intercept('GET', '**/users/999', {
      statusCode: 404,
      body: { error: 'Utilisateur non trouvé' },
    }).as('userNotFound')

    cy.request({
      url: 'https://jsonplaceholder.typicode.com/users/999',
      failOnStatusCode: false,  // ne pas faire échouer le test sur 404
    }).then((response) => {
      // jsonplaceholder retourne 200 avec {} pour les IDs inexistants
      // Dans une vraie app, on testerait ici le message d'erreur affiché
    })
  })

  it('modifier dynamiquement une réponse avec req.reply()', () => {
    cy.intercept('GET', '**/todos/1', (req) => {
      req.reply((res) => {
        // Modifie la vraie réponse avant de la renvoyer au navigateur
        res.body.completed = true
        res.body.title = 'Titre modifié par Cypress'
      })
    }).as('todoModifie')
  })
})
