// MODULE 1 — ASSERTIONS
//
// Cypress utilise la bibliothèque Chai pour les assertions.
// La syntaxe .should('...') est identique aux matchers BDD de Cucumber.

describe('Module 1 : Assertions Cypress / Chai', () => {
  before(() => {
    cy.visit('/')
  })

  // ─── Assertions sur les éléments DOM ───────────────────────────────────────

  it('assertions d\'existence et visibilité', () => {
    cy.get('.navbar-brand').should('exist')
    cy.get('.navbar-brand').should('be.visible')
    cy.get('#non-existant').should('not.exist')
  })

  it('assertions sur le texte', () => {
    cy.get('.navbar-brand').should('contain', 'Cypress')
    cy.get('.navbar-brand').should('have.text', 'cypress.io')
    // .include.text est plus souple (sous-chaîne)
    cy.get('.navbar-brand').should('include.text', 'cypress')
  })

  it('assertions sur les attributs HTML', () => {
    cy.get('.navbar-brand').should('have.attr', 'href')
    cy.get('.navbar-brand').should('have.attr', 'href', '/')
  })

  it('assertions sur les classes CSS', () => {
    cy.get('.navbar').should('have.class', 'navbar')
    cy.get('.navbar').should('not.have.class', 'hidden')
  })

  it('assertions sur des listes (length)', () => {
    cy.get('.home-list li').should('have.length.greaterThan', 3)
    cy.get('.home-list li').should('have.length.at.least', 1)
  })

  // ─── Assertions sur des valeurs JavaScript ──────────────────────────────────

  it('assertions avec .then() pour valeurs dynamiques', () => {
    cy.get('.navbar-brand').invoke('text').then((texte) => {
      // Ici on sort de la chaîne Cypress et on entre dans JS pur
      expect(texte).to.include('cypress')
      expect(texte.length).to.be.greaterThan(0)
    })
  })

  it('vérifier plusieurs assertions en une seule commande', () => {
    // .should() accepte une fonction callback
    cy.get('.navbar').should(($el) => {
      expect($el).to.be.visible
      expect($el.hasClass('navbar')).to.be.true
    })
  })
})
