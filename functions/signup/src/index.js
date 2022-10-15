const sdk = require("node-appwrite")
const sgMail = require("@sendgrid/mail")

module.exports = async function (req, res) {
  const client = new sdk.Client()

  const database = new sdk.Databases(client)

  client
    .setEndpoint(req.variables["APPWRITE_FUNCTION_ENDPOINT"])
    .setProject(req.variables["APPWRITE_FUNCTION_PROJECT_ID"])
    .setKey(req.variables["APPWRITE_FUNCTION_API_KEY"])
    .setSelfSigned(true)

  const payload = JSON.parse(req.payload)

  const search = await database.listDocuments(
    req.variables["DATABASE_ID"],
    req.variables["COLLECTION_ID"],
    [sdk.Query.equal("email", payload["email"])]
  )

  if (search.documents.length > 0) {
    res.json({
      create: false,
      msg: search.documents[0].verified
        ? "Already signed up with this email, please log in!"
        : "Already signed up with this email, please verify it then log in!",
    })
  } else {
    try {
      const rand = Math.floor(100000 + Math.random() * 900000)

      await database.createDocument(
        req.variables["DATABASE_ID"],
        req.variables["COLLECTION_ID"],
        sdk.ID.unique(),
        {
          email: payload["email"],
          otp: rand,
          pwd: payload["pwd"],
          verified: false,
        }
      )

      sgMail.setApiKey(req.variables["SENDGRID_API_KEY"])

      const msg = {
        to: payload["email"],
        from: req.variables["SENDGRID_EMAIL_FROM"],
        subject: "Welcome to Cowboy Nukem 3D! 👋",
        text: `Please input this OTP in your game to verify this email: ${rand}`,
        html: `<h3>Please input this OTP in your game to verify this email: ${rand}</h3>`,
      }

      try {
        await sgMail.send(msg)
        res.json({
          create: true,
          msg: "User created, verification email sent!",
        })
      } catch (e) {
        res.json({
          create: false,
          msg: e.message,
        })
      }
    } catch (e) {
      res.json({
        create: false,
        msg: e.message,
      })
    }
  }
}
