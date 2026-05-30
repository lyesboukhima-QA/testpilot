// MODULE 2 — NAVIGATION AVANCÉE
// Attentes, retour arrière, iframes, aliases

describe('Module 2 : Navigation avancée', () => {

  it('attente automatique (retry-ability)', () => {
    cy.visit('/commands/waiting')

    // Cypress réessaie automatiquement jusqu'à defaultCommandTimeout
    // PAS besoin de cy.wait(3000) pour les éléments DOM !
    cy.get('#wait-for-selector').should('be.visible')

    // cy.wait() est réservé aux délais explicites ou aux aliases réseau
    // cy.wait(500) = OK si vraiment nécessaire (à éviter)
  })

  it('alias — réutiliser un élément', () => {
    cy.visit('/commands/querying')

    // .as() crée un alias, @alias le rappelle plus tard
    cy.get('.query-table tbody tr').as('lignes')

    cy.get('@lignes').should('have.length.greaterThan', 0)
    cy.get('@lignes').first().should('be.visible')
  })

  it('parcourir une liste avec .each()', () => {
    cy.visit('/commands/querying')

    cy.get('.query-table tbody tr').each(($ligne, index) => {
      cy.wrap($ligne).should('be.visible')
      cy.log(`Ligne ${index + 1} visible`)
    })
  })

  it('naviguer dans le DOM avec .within()', () => {
    cy.visit('/commands/querying')

    // .within() limite la portée des sélecteurs suivants
    cy.get('.query-table').within(() => {
      cy.get('tbody tr').should('exist')
      cy.get('thead').should('contain', 'Name')
    })
  })

  it('retour arrière et en avant', () => {
    cy.visit('/')
    cy.visit('/commands/actions')
    cy.go('back')
    cy.url().should('eq', Cypress.config('baseUrl') + '/')
    cy.go('forward')
    cy.url().should('include', '/commands/actions')
  })

  it('recharger la page', () => {
    cy.visit('/commands/actions')
    cy.reload()
    cy.url().should('include', '/commands/actions')
  })

  it('récupérer plusieurs éléments avec .find()', () => {
    cy.visit('/commands/querying')

    // .find() = chercher à l'intérieur d'un élément parent
    cy.get('.query-table').find('tbody tr').should('have.length.greaterThan', 0)
  })
})
