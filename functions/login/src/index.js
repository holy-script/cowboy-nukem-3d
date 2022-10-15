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
      signin: false,
      msg: "Email does not exist, please sign up, verify email, then try logging in again!",
    })
  } else {
    if (!search.documents[0].verified)
      res.json({
        signin: false,
        msg: "Email not verified, play use the OTP sent to confirm it and then log in!",
      })
    search.documents[0].pwd == payload["pwd"]
      ? res.json({
          signin: true,
          msg: "Welcome, have fun playing in online mode!",
        })
      : res.json({
          signin: false,
          msg: "Password incorrect, please try logging in again!",
        })
  }
}
