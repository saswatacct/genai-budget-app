require('dotenv').config()

const express = require('express')
const bodyParser = require('body-parser')
const session = require('express-session')

const app = express()

app.set('view engine', 'ejs')

app.use(express.static('public'))

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.use(session({
  secret: process.env.SESSION_SECRET || 'smartspend-local-secret',
  resave: false,
  saveUninitialized: false
}))

const webRoutes = require('./routes/web')

app.use('/', webRoutes)

const PORT = process.env.PORT || 3000

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Web app running on port ${PORT}`)
})