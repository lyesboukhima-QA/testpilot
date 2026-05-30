// MODULE 1 — BASES : Navigation et assertions fondamentales
//
// Cypress vs ce que tu connais :
//   Robot Framework  →  cy.visit()  =  Open Browser + Go To
//   Cucumber step    →  cy.get()    =  Find Element
//   Assert Should    →  .should()   =  assertions chainées

describe('Module 1 : Navigation de base', () => {
  // beforeEach = équivalent de [Test Setup] en Robot Framework
  beforeEach(() => {
    cy.visit('/')  // utilise baseUrl défini dans cypress.config.js
  })

  it('visite la page d\'accueil et vérifie le titre', () => {
    // cy.title() récupère le <title> de la page
    cy.title().should('include', 'Cypress')

    // cy.url() vérifie l'URL courante
    cy.url().should('include', 'example.cypress.io')
  })

  it('navigue vers une sous-page', () => {
    cy.visit('/commands/actions')

    // Vérifie que la page s'est chargée
    cy.url().should('include', '/commands/actions')
  })

  it('vérifie qu\'un élément existe sur la page', () => {
    // cy.get() = sélecteur CSS (équivalent de Get WebElement en Robot)
    cy.get('.navbar').should('exist')
    cy.get('.navbar').should('be.visible')

    // Chaînage : plus concis
    cy.get('.navbar').should('exist').and('be.visible')
  })

  it('vérifie le contenu textuel d\'un élément', () => {
    cy.visit('/commands/querying')

    // .contains() cherche un texte dans la page
    cy.contains('Querying').should('be.visible')

    // Sélecteur + texte combinés
    cy.get('h1').contains('Querying')
  })

  it('utilise les sélecteurs data-cy (bonne pratique)', () => {
    // En Cypress, la convention recommandée est d'utiliser
    // data-cy="nom" dans le HTML pour cibler les éléments de test
    // Ex : <button data-cy="submit-btn">
    // cy.get('[data-cy="submit-btn"]').click()

    // Sur le site demo, on utilise les classes disponibles
    cy.get('.home-list').should('exist')
    cy.get('.home-list li').should('have.length.greaterThan', 0)
  })
})
