// MODULE 4 — BDD avec Cypress
//
// Comme tu connais Cucumber/Gherkin, voici comment structurer
// tes tests Cypress en style BDD SANS plugin supplémentaire.
//
// Pour un vrai support Gherkin (.feature files), installe :
//   npm install --save-dev @badeball/cypress-cucumber-preprocessor
//
// Ici on montre le style BDD natif Cypress.

describe('Module 4 : Style BDD — Given / When / Then', () => {

  // ─── Scénario 1 ────────────────────────────────────────────────────────────
  context('Étant donné que je consulte la liste des posts', () => {

    before(() => {
      // GIVEN : état initial
      cy.request('https://jsonplaceholder.typicode.com/posts')
        .as('listePosts')
    })

    it('WHEN je récupère tous les posts THEN j\'en reçois 100', () => {
      cy.get('@listePosts').its('body').should('have.length', 100)
    })

    it('WHEN j\'inspecte le premier post THEN il a un titre', () => {
      cy.get('@listePosts').its('body.0').should('have.property', 'title')
    })
  })

  // ─── Scénario 2 ────────────────────────────────────────────────────────────
  context('Étant donné que je navigue sur le site Cypress', () => {

    beforeEach(() => {
      // GIVEN
      cy.visit('https://example.cypress.io')
    })

    it('WHEN la page se charge THEN le logo est visible', () => {
      // THEN
      cy.get('.navbar-brand').should('be.visible')
    })

    it('WHEN je clique sur "Actions" THEN la page s\'affiche', () => {
      // WHEN
      cy.get('.home-list').contains('Actions').click()

      // THEN
      cy.url().should('include', '/commands/actions')
      cy.get('h1').should('contain', 'Actions')
    })
  })
})

// ─── Avec le vrai plugin Cucumber (@badeball/cypress-cucumber-preprocessor) ──
//
// 1. npm install @badeball/cypress-cucumber-preprocessor @bahmutov/cypress-esbuild-preprocessor
//
// 2. cypress/e2e/login.feature :
//    Feature: Connexion utilisateur
//      Scenario: Connexion réussie
//        Given je suis sur la page de login
//        When je saisis "admin@test.com" et "password123"
//        Then je suis redirigé vers le dashboard
//
// 3. cypress/e2e/login.js (step definitions) :
//    import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor"
//    Given("je suis sur la page de login", () => { cy.visit('/login') })
//    When("je saisis {string} et {string}", (email, mdp) => {
//      cy.get('#email').type(email)
//      cy.get('#password').type(mdp)
//      cy.get('[type=submit]').click()
//    })
//    Then("je suis redirigé vers le dashboard", () => {
//      cy.url().should('include', '/dashboard')
//    })
