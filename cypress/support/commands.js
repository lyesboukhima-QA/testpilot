// COMMANDES PERSONNALISÉES CYPRESS
// Équivalent des Keywords en Robot Framework.
// Toutes les commandes définies ici sont disponibles via cy.nomCommande()

// ─── cy.connexion(email, motDePasse) ───────────────────────────────────────
// Simule un login via formulaire.
// Utilisation : cy.connexion('user@test.com', 'secret')
Cypress.Commands.add('connexion', (email, motDePasse) => {
  cy.visit('/login')
  cy.get('#email').type(email)
  cy.get('#password').type(motDePasse, { log: false }) // log:false masque le mdp dans les logs
  cy.get('[type="submit"]').click()
})

// ─── cy.connexionAPI(email, motDePasse) ────────────────────────────────────
// Login via API (plus rapide que via UI — recommandé pour les tests non-auth)
Cypress.Commands.add('connexionAPI', (email, motDePasse) => {
  cy.request('POST', '/api/login', { email, password: motDePasse })
    .then(({ body }) => {
      window.localStorage.setItem('token', body.token)
    })
})

// ─── cy.verifierApi(url, propriétésAttendues) ──────────────────────────────
// Raccourci pour vérifier une réponse API.
// Utilisation : cy.verifierApi('/api/users/1', { id: 1, email: 'a@b.com' })
Cypress.Commands.add('verifierApi', (url, proprietesAttendues) => {
  cy.request(url).then((response) => {
    expect(response.status).to.eq(200)
    Object.entries(proprietesAttendues).forEach(([cle, valeur]) => {
      expect(response.body[cle]).to.eq(valeur)
    })
  })
})

// ─── cy.remplirFormulaire(données) ─────────────────────────────────────────
// Remplit un formulaire à partir d'un objet.
// Utilisation : cy.remplirFormulaire({ '#nom': 'Lyes', '#email': 'l@t.com' })
Cypress.Commands.add('remplirFormulaire', (donnees) => {
  Object.entries(donnees).forEach(([selecteur, valeur]) => {
    cy.get(selecteur).clear().type(valeur)
  })
})
