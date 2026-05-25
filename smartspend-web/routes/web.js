const express = require('express')
const axios = require('axios')

const router = express.Router()

const API = process.env.BACKEND_URL


// ======================================
// HOME
// ======================================

router.get('/', (req, res) => {

    res.redirect('/login')

})


// ======================================
// LOGIN
// ======================================

router.get('/login', (req, res) => {

    res.render('login')

})

router.post('/login', async (req, res) => {

    try {

        const response = await axios.post(

            `${API}/auth/login`,

            {

                email:
                    req.body.email,

                password:
                    req.body.password

            }

        )

        req.session.token =

            response.data
                .access_token

        res.redirect(
            '/dashboard'
        )

    }

    catch (err) {

        console.log(

            err.response?.data

        )

        res.send(

            err.response
                ?.data
                ?.detail ||

            'Login Failed'

        )

    }

})


// ======================================
// SIGNUP
// ======================================

router.get('/signup', (req, res) => {

    res.render(
        'signup'
    )

})

router.post('/signup', async (req, res) => {

    try {

        const password =

            req.body.password
                ?.trim()

        if (
            password.length > 72
        ) {

            return res.send(

                'Password cannot exceed 72 characters'

            )

        }

        const response =
            await axios.post(

                `${API}/auth/signup`,

                {

                    name:
                        req.body.name,

                    email:
                        req.body.email,

                    password,

                    phone:
                        req.body.phone

                }

            )

        req.session.token =

            response.data
                .access_token

        res.redirect(
            '/dashboard'
        )

    }

    catch (err) {

        console.log(

            err.response?.data

        )

        res.send(

            err.response
                ?.data
                ?.detail ||

            'Signup Failed'

        )

    }

})


// ======================================
// FORGOT PASSWORD
// ======================================

router.get(
    '/forgot-password',
    (req, res) => {

        res.render(
            'forgot_password'
        )

    }
)


router.post(
    '/forgot-password',
    async (req, res) => {

        try {

            await axios.post(

                `${API}/auth/forgot-password`,

                {

                    email:
                        req.body.email

                }

            )

            res.send(

                `
                Password reset link
                sent to WhatsApp.

                Please check
                your WhatsApp.
                `

            )

        }

        catch (err) {

            console.log(

                err.response?.data

            )

            res.send(

                err.response
                    ?.data
                    ?.detail ||

                'Unable to process request'

            )

        }

    }
)


// ======================================
// RESET PASSWORD
// ======================================

router.get(
    '/reset-password',
    (req, res) => {

        const token =
            req.query.token

        if (!token) {

            return res.send(

                'Invalid reset link'

            )

        }

        res.render(

            'reset_password',

            {

                token

            }

        )

    }
)


router.post(
    '/reset-password',
    async (req, res) => {

        try {

            const token =

                req.body.token
                    ?.trim()

            const password =

                req.body.password
                    ?.trim()

            if (

                !token

            ) {

                return res.send(

                    'Reset token missing'

                )

            }

            if (

                !password

            ) {

                return res.send(

                    'Password required'

                )

            }

            if (

                password.length < 8

            ) {

                return res.send(

                    'Password minimum 8 characters'

                )

            }

            if (

                password.length > 72

            ) {

                return res.send(

                    'Password cannot exceed 72 characters'

                )

            }

            await axios.post(

                `${API}/auth/reset-password`,

                {

                    token,

                    password

                }

            )

            res.send(

                `
                Password updated.

                Please login again.
                `

            )

        }

        catch (err) {

            console.log(

                'RESET ERROR:',

                err.response?.data ||

                err.message

            )

            res.send(

                err.response
                    ?.data
                    ?.detail ||

                'Password reset failed'

            )

        }

    }
)


// ======================================
// DASHBOARD
// ======================================

router.get('/dashboard', (req, res) => {

    if (
        !req.session.token
    ) {

        return res.redirect(
            '/login'
        )

    }

    res.render(
        'dashboard'
    )

})


// ======================================
// LIMIT
// ======================================

router.get('/limit', (req, res) => {

    if (
        !req.session.token
    ) {

        return res.redirect(
            '/login'
        )

    }

    res.render(
        'limit'
    )

})

router.post('/limit', async (req, res) => {

    try {

        await axios.post(

            `${API}/limit/create`,

            {

                upi_limit:

                    Number(
                        req.body.upi_limit
                    ),

                credit_limit:

                    Number(
                        req.body.credit_limit
                    ),

                card_no:
                    req.body.card_no,

                account_no:
                    req.body.account_no,

                atm_enabled:

                    req.body
                        .atm_enabled
                    === 'on',

                online_enabled:

                    req.body
                        .online_enabled
                    === 'on'

            },

            {

                headers: {

                    Authorization:

                        `Bearer ${req.session.token}`

                }

            }

        )

        res.redirect(
            '/dashboard'
        )

    }

    catch (err) {

        console.log(

            err.response?.data

        )

        res.send(

            'Limit Error'

        )

    }

})


// ======================================
// TRANSACTION
// ======================================

router.get('/transaction', (req, res) => {

    if (
        !req.session.token
    ) {

        return res.redirect(
            '/login'
        )

    }

    res.render(

        'transaction',

        {

            response: null

        }

    )

})


router.post('/transaction', async (req, res) => {

    try {

        const response =
            await axios.post(

                `${API}/transaction/add`,

                {

                    amount:

                        Number(
                            req.body.amount
                        ),

                    merchant:

                        req.body.merchant,

                    txn_mode:

                        req.body.txn_mode,

                    payment_mode:

                        req.body.payment_mode

                },

                {

                    headers: {

                        Authorization:

                            `Bearer ${req.session.token}`

                    }

                }

            )

        res.render(

            'transaction',

            {

                response:
                    response.data

            }

        )

    }

    catch (err) {

        console.log(

            err.response?.data

        )

        res.send(

            err.response
                ?.data
                ?.detail ||

            'Transaction Error'

        )

    }

})


// ======================================
// HISTORY
// ======================================

router.get('/history', async (req, res) => {

    try {

        const response =
            await axios.get(

                `${API}/history/transactions`,

                {

                    headers: {

                        Authorization:

                            `Bearer ${req.session.token}`

                    }

                }

            )

        res.render(

            'history',

            {

                transactions:

                    response.data
                        .transactions

            }

        )

    }

    catch (err) {

        console.log(

            err.response?.data

        )

        res.send(

            'History Error'

        )

    }

})


// ======================================
// DELETE
// ======================================

router.post(
    '/transaction/delete/:id',

    async (req, res) => {

        try {

            await axios.delete(

                `${API}/transaction/delete/${req.params.id}`,

                {

                    headers: {

                        Authorization:

                            `Bearer ${req.session.token}`

                    }

                }

            )

            res.redirect(
                '/history'
            )

        }

        catch (err) {

            console.log(

                err.response?.data

            )

            res.send(

                'Delete Failed'

            )

        }

    })


// ======================================
// LOGOUT
// ======================================

router.get('/logout', (req, res) => {

    req.session.destroy(() => {

        res.redirect(
            '/login'
        )

    })

})


module.exports = router