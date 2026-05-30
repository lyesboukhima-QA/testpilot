// MODULE 2 — INTERACTIONS : Formulaires et clics
//
// Cypress vs Robot Framework :
//   Input Text      →  cy.type()
//   Click Element   →  cy.click()
//   Select From List→  cy.select()
//   Clear Element   →  cy.clear()

describe('Module 2 : Interactions avec les formulaires', () => {

  it('saisie de texte dans un champ', () => {
    cy.visit('/commands/actions')

    // .type() simule la frappe clavier
    cy.get('.action-email').type('lyes@example.com')

    // Vérifie que la valeur est bien saisie
    cy.get('.action-email').should('have.value', 'lyes@example.com')
  })

  it('effacer et re-saisir', () => {
    cy.visit('/commands/actions')

    cy.get('.action-email').type('premier texte')
    cy.get('.action-email').clear()
    cy.get('.action-email').should('have.value', '')

    cy.get('.action-email').type('deuxième texte')
    cy.get('.action-email').should('have.value', 'deuxième texte')
  })

  it('touches spéciales dans .type()', () => {
    cy.visit('/commands/actions')

    // Touches spéciales entre accolades
    cy.get('.action-email').type('test{enter}')
    cy.get('.action-email').type('{selectall}{del}')
    cy.get('.action-email').type('texte{backspace}')
    // Autres : {tab}, {esc}, {uparrow}, {downarrow}, {ctrl}A
  })

  it('clic simple', () => {
    cy.visit('/commands/actions')

    cy.get('.action-btn').click()
    // Après un clic, on vérifie le résultat attendu
    // cy.get('.feedback').should('contain', 'clicked')
  })

  it('double-clic et clic-droit', () => {
    cy.visit('/commands/actions')

    cy.get('.action-div').dblclick()
    cy.get('.action-div').rightclick()
  })

  it('sélectionner dans une liste déroulante', () => {
    cy.visit('/commands/actions')

    // .select() par texte visible ou par value
    cy.get('.action-select').select('apples')
    cy.get('.action-select').should('have.value', 'fr-apples')

    cy.get('.action-select').select('fr-oranges')
    cy.get('.action-select').should('have.value', 'fr-oranges')
  })

  it('cocher / décocher une case', () => {
    cy.visit('/commands/actions')

    cy.get('.action-checkboxes [type="checkbox"]').first().check()
    cy.get('.action-checkboxes [type="checkbox"]').first().should('be.checked')

    cy.get('.action-checkboxes [type="checkbox"]').first().uncheck()
    cy.get('.action-checkboxes [type="checkbox"]').first().should('not.be.checked')
  })

  it('bouton radio', () => {
    cy.visit('/commands/actions')

    cy.get('.action-radios [type="radio"]').first().check()
    cy.get('.action-radios [type="radio"]').first().should('be.checked')
  })
})
