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
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}))

const webRoutes = require('./routes/web')

app.use('/', webRoutes)

app.listen(process.env.PORT, () => {
  console.log(`Web app running on port ${process.env.PORT}`)
})