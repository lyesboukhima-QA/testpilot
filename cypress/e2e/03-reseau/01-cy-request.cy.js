// MODULE 3 — RÉSEAU : cy.request() — Tests d'API
//
// Comme tu connais Robot Framework + RequestsLibrary,
// cy.request() va te sembler très familier.
//
// Robot:  GET  ${URL}    →  Cypress: cy.request('GET', url)
// Robot:  Should Be Equal As Integers  ${status}  200
//         →  Cypress: .its('status').should('eq', 200)

describe('Module 3 : Tests API avec cy.request()', () => {
  const API = 'https://jsonplaceholder.typicode.com'

  it('GET simple — vérifier le status et le corps', () => {
    cy.request('GET', `${API}/todos/1`).then((response) => {
      expect(response.status).to.eq(200)
      expect(response.body).to.have.property('id', 1)
      expect(response.body).to.have.property('title')
      expect(response.body.completed).to.be.a('boolean')
    })
  })

  it('GET avec .its() — syntaxe chaînée', () => {
    cy.request(`${API}/users/1`)
      .its('status').should('eq', 200)

    cy.request(`${API}/users/1`)
      .its('body.email').should('include', '@')
  })

  it('GET une liste — vérifier la longueur', () => {
    cy.request(`${API}/todos`)
      .its('body')
      .should('have.length', 200)
      .its('0')
      .should('have.property', 'userId')
  })

  it('POST — créer une ressource', () => {
    cy.request({
      method: 'POST',
      url: `${API}/posts`,
      body: {
        title: 'Mon titre Cypress',
        body: 'Contenu du post',
        userId: 1,
      },
      headers: {
        'Content-Type': 'application/json',
      },
    }).then((response) => {
      expect(response.status).to.eq(201)
      expect(response.body).to.have.property('id')
      expect(response.body.title).to.eq('Mon titre Cypress')
    })
  })

  it('PUT — modifier une ressource', () => {
    cy.request({
      method: 'PUT',
      url: `${API}/posts/1`,
      body: { title: 'Titre modifié', body: 'Corps modifié', userId: 1 },
    }).its('status').should('eq', 200)
  })

  it('DELETE — supprimer une ressource', () => {
    cy.request({
      method: 'DELETE',
      url: `${API}/posts/1`,
    }).its('status').should('eq', 200)
  })

  it('vérifier un header de réponse', () => {
    cy.request(`${API}/posts/1`).then((response) => {
      expect(response.headers['content-type']).to.include('application/json')
    })
  })
})
