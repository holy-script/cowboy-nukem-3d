const sdk = require("node-appwrite")

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

  if (search.documents.length == 0) {
    res.json({
      verify: false,
      msg: "Email does not exist, please sign up and then verify the email!",
    })
  } else {
    if (search.documents[0].verified)
      res.json({
        verify: false,
        msg: "Email already verified, please log in!",
      })
    if (search.documents[0].otp == payload["otp"]) {
      try {
        await database.updateDocument(
          req.variables["DATABASE_ID"],
          req.variables["COLLECTION_ID"],
          search.documents[0].$id,
          {
            verified: true,
          }
        )
        res.json({
          verify: true,
          msg: "Email verified successful, please log in now!",
        })
      } catch (e) {
        res.json({
          verify: false,
          msg: e.message,
        })
      }
    } else {
      res.json({
        verify: false,
        msg: "Incorrect OTP, please try verification again!",
      })
    }
  }
}
