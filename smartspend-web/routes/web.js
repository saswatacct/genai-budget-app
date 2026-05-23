// const express = require('express')
// const axios = require('axios')

// const router = express.Router()

// const API = process.env.BACKEND_URL


// // ======================================
// // HOME
// // ======================================

// router.get('/', (req, res) => {

//     res.redirect('/login')
// })


// // ======================================
// // LOGIN
// // ======================================

// router.get('/login', (req, res) => {

//     res.render('login')
// })

// router.post('/login', async (req, res) => {

//     try {

//         const response = await axios.post(
//             `${API}/auth/login`,
//             {
//                 email: req.body.email,
//                 password: req.body.password
//             }
//         )

//         req.session.token =
//             response.data.access_token

//         res.redirect('/dashboard')

//     } catch (err) {

//         console.log(err.response?.data)

//         res.send('Login Failed')
//     }
// })


// // ======================================
// // SIGNUP
// // ======================================

// router.get('/signup', (req, res) => {

//     res.render('signup')
// })

// router.post('/signup', async (req, res) => {

//     try {

//         const response = await axios.post(
//             `${API}/auth/signup`,
//             {
//                 name: req.body.name,
//                 email: req.body.email,
//                 password: req.body.password,
//                 phone: req.body.phone
//             }
//         )

//         req.session.token =
//             response.data.access_token

//         res.redirect('/dashboard')

//     } catch (err) {

//         console.log(err.response?.data)

//         res.send('Signup Failed')
//     }
// })


// // ======================================
// // DASHBOARD
// // ======================================

// router.get('/dashboard', (req, res) => {

//     if (!req.session.token) {

//         return res.redirect('/login')
//     }

//     res.render('dashboard')
// })


// // ======================================
// // LIMIT SETUP
// // ======================================

// router.get('/limit', (req, res) => {

//     if (!req.session.token) {

//         return res.redirect('/login')
//     }

//     res.render('limit')
// })

// router.post('/limit', async (req, res) => {

//     try {

//         await axios.post(
//             `${API}/limit/create`,
//             {
//                 upi_limit:
//                     Number(req.body.upi_limit),

//                 credit_limit:
//                     Number(req.body.credit_limit),

//                 card_no:
//                     req.body.card_no,

//                 account_no:
//                     req.body.account_no,

//                 atm_enabled:
//                     req.body.atm_enabled === 'on',

//                 online_enabled:
//                     req.body.online_enabled === 'on'
//             },
//             {
//                 headers: {
//                     Authorization:
//                         `Bearer ${req.session.token}`
//                 }
//             }
//         )

//         res.redirect('/dashboard')

//     } catch (err) {

//         console.log(err.response?.data)

//         res.send(
//             err.response?.data || 'Limit Error'
//         )
//     }
// })


// // ======================================
// // ADD TRANSACTION
// // ======================================

// router.get('/transaction', (req, res) => {

//     if (!req.session.token) {

//         return res.redirect('/login')
//     }

//     res.render('transaction', {
//         response: null
//     })
// })

// router.post('/transaction', async (req, res) => {

//     try {

//         const response = await axios.post(
//             `${API}/transaction/add`,
//             {
//                 amount:
//                     Number(req.body.amount),

//                 merchant:
//                     req.body.merchant,

//                 txn_mode:
//                     req.body.txn_mode,

//                 payment_mode:
//                     req.body.payment_mode
//             },
//             {
//                 headers: {
//                     Authorization:
//                         `Bearer ${req.session.token}`
//                 }
//             }
//         )

//         res.render('transaction', {
//             response: response.data
//         })

//     } catch (err) {

//         console.log(err.response?.data)

//         res.send(
//             err.response?.data || 'Transaction Error'
//         )
//     }
// })


// // ======================================
// // TRANSACTION HISTORY
// // ======================================

// router.get('/history', async (req, res) => {

//     try {

//         const response = await axios.get(
//             `${API}/history/transactions`,
//             {
//                 headers: {
//                     Authorization:
//                         `Bearer ${req.session.token}`
//                 }
//             }
//         )

//         res.render('history', {
//             transactions:
//                 response.data.transactions
//         })

//     } catch (err) {

//         console.log(err.response?.data)

//         res.send(
//             'Failed to load transaction history'
//         )
//     }
// })


// // ======================================
// // DELETE TRANSACTION
// // ======================================

// router.post(
//     '/transaction/delete/:id',
//     async (req, res) => {

//         try {

//             await axios.delete(
//                 `${API}/transaction/delete/${req.params.id}`,
//                 {
//                     headers: {
//                         Authorization:
//                             `Bearer ${req.session.token}`
//                     }
//                 }
//             )

//             res.redirect('/history')

//         } catch (err) {

//             console.log(err.response?.data)

//             res.send('Delete failed')
//         }
//     }
// )


// // ======================================
// // LOGOUT
// // ======================================

// router.get('/logout', (req, res) => {

//     req.session.destroy(() => {

//         res.redirect('/login')
//     })
// })


// // ======================================
// // EXPORT ROUTER
// // ======================================

// module.exports = router



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

    catch(err){

        console.log(

            err.response?.data

        )

        res.send(
            'Login Failed'
        )

    }

})


// ======================================
// SIGNUP
// ======================================

router.get('/signup',(req,res)=>{

    res.render(
        'signup'
    )

})

router.post('/signup',async(req,res)=>{

    try{

        const response =
        await axios.post(

            `${API}/auth/signup`,

            {

                name:
                req.body.name,

                email:
                req.body.email,

                password:
                req.body.password,

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

    catch(err){

        console.log(

            err.response?.data

        )

        res.send(
            'Signup Failed'
        )

    }

})


// ======================================
// FORGOT PASSWORD
// ======================================

router.get(
    '/forgot-password',
    (req,res)=>{

        res.render(
            'forgot_password'
        )

    }
)


router.post(
    '/forgot-password',
    async(req,res)=>{

        try{

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

        catch(err){

            console.log(

                err.response?.data

            )

            res.send(

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
    (req,res)=>{

        res.render(

            'reset_password',

            {

                token:
                req.query.token

            }

        )

    }
)


router.post(
    '/reset-password',
    async(req,res)=>{

        try{

            await axios.post(

                `${API}/auth/reset-password`,

                {

                    token:
                    req.body.token,

                    password:
                    req.body.password

                }

            )

            res.send(

                `
                Password updated.

                Please login again.
                `

            )

        }

        catch(err){

            console.log(

                err.response?.data

            )

            res.send(

                'Password reset failed'

            )

        }

    }
)


// ======================================
// DASHBOARD
// ======================================

router.get('/dashboard',(req,res)=>{

    if(
        !req.session.token
    ){

        return res.redirect(
            '/login'
        )

    }

    res.render(
        'dashboard'
    )

})


// ======================================
// LIMIT SETUP
// ======================================

router.get('/limit',(req,res)=>{

    if(
        !req.session.token
    ){

        return res.redirect(
            '/login'
        )

    }

    res.render(
        'limit'
    )

})


router.post('/limit',async(req,res)=>{

    try{

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

                headers:{

                    Authorization:

                    `Bearer ${req.session.token}`

                }

            }

        )

        res.redirect(
            '/dashboard'
        )

    }

    catch(err){

        console.log(

            err.response?.data

        )

        res.send(

            err.response?.data ||

            'Limit Error'

        )

    }

})


// ======================================
// TRANSACTION
// ======================================

router.get('/transaction',(req,res)=>{

    if(
        !req.session.token
    ){

        return res.redirect(
            '/login'
        )

    }

    res.render(

        'transaction',

        {

            response:null

        }

    )

})


router.post('/transaction',async(req,res)=>{

    try{

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

                headers:{

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

    catch(err){

        console.log(

            err.response?.data

        )

        res.send(

            err.response?.data ||

            'Transaction Error'

        )

    }

})


// ======================================
// HISTORY
// ======================================

router.get('/history',async(req,res)=>{

    try{

        const response =
        await axios.get(

            `${API}/history/transactions`,

            {

                headers:{

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

    catch(err){

        console.log(

            err.response?.data

        )

        res.send(

            'Failed to load history'

        )

    }

})


// ======================================
// DELETE TRANSACTION
// ======================================

router.post(
'/transaction/delete/:id',

async(req,res)=>{

    try{

        await axios.delete(

            `${API}/transaction/delete/${req.params.id}`,

            {

                headers:{

                    Authorization:

                    `Bearer ${req.session.token}`

                }

            }

        )

        res.redirect(
            '/history'
        )

    }

    catch(err){

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

router.get('/logout',(req,res)=>{

    req.session.destroy(()=>{

        res.redirect(
            '/login'
        )

    })

})


// ======================================
// EXPORT
// ======================================

module.exports = router