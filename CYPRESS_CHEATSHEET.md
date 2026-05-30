# Cypress — Cheat Sheet (pour qui connaît Robot Framework / Cucumber)

## Équivalences Robot Framework → Cypress

| Robot Framework          | Cypress                            |
|--------------------------|------------------------------------|
| `Open Browser`           | `cy.visit('https://...')`          |
| `Go To`                  | `cy.visit('/page')`                |
| `Get WebElement`         | `cy.get('.selector')`              |
| `Input Text`             | `cy.get('#champ').type('texte')`   |
| `Click Element`          | `cy.get('btn').click()`            |
| `Select From List`       | `cy.get('select').select('val')`   |
| `Clear Element Text`     | `cy.get('#champ').clear()`         |
| `Should Contain`         | `.should('contain', 'texte')`      |
| `Should Be Equal`        | `.should('eq', valeur)`            |
| `Should Be Visible`      | `.should('be.visible')`            |
| `[Test Setup]`           | `beforeEach(() => { ... })`        |
| `[Test Teardown]`        | `afterEach(() => { ... })`         |
| `GET ${url}`             | `cy.request('GET', url)`           |
| `Keyword`                | `Cypress.Commands.add('nom', fn)`  |
| Variable `${DATA}`       | `cy.fixture('fichier').as('DATA')` |

## Structure d'un test Cypress

```js
describe('Nom du groupe (= Test Suite)', () => {
  before(() => { /* s'exécute 1 fois avant tous les tests */ })
  beforeEach(() => { /* s'exécute avant chaque test */ })
  after(() => { /* s'exécute 1 fois après tous les tests */ })
  afterEach(() => { /* s'exécute après chaque test */ })

  it('nom du test', () => {
    // ton test ici
  })
})
```

## Sélecteurs (par ordre de préférence)

```js
cy.get('[data-cy="submit"]')    // ← MEILLEURE PRATIQUE
cy.get('#id')
cy.get('.classe')
cy.get('input[name="email"]')
cy.contains('Texte visible')    // trouve par texte
cy.get('ul').find('li').first() // chaîner
```

## Assertions fréquentes

```js
.should('exist')
.should('be.visible')
.should('not.exist')
.should('be.disabled')
.should('have.value', 'texte')
.should('contain', 'sous-texte')
.should('have.text', 'texte exact')
.should('have.class', 'active')
.should('have.attr', 'href', '/page')
.should('have.length', 5)
.should('eq', 42)              // égalité stricte
.should('include', 'partie')   // chaîne contient
```

## API Testing

```js
cy.request('https://api.example.com/users')
  .its('status').should('eq', 200)

cy.request({ method: 'POST', url: '/api/users', body: { name: 'Lyes' } })
  .then(res => { expect(res.body.id).to.exist })
```

## Mock réseau (intercept)

```js
// Avant de visiter la page !
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers')
cy.visit('/dashboard')
cy.wait('@getUsers')  // attend que la vraie requête passe
```

## Commandes personnalisées

```js
// cypress/support/commands.js
Cypress.Commands.add('login', (email, pwd) => {
  cy.get('#email').type(email)
  cy.get('#pwd').type(pwd)
  cy.get('[type=submit]').click()
})

// Dans les tests :
cy.login('user@test.com', 'secret')
```

## Lancer les tests

```bash
npm run cy:open          # Interface graphique (développement)
npm run cy:run           # Ligne de commande (CI/CD)
npm run cy:run:module1   # Seulement le module 1
```
