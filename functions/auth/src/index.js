const sdk = require("node-appwrite")

module.exports = async function (req, res) {
  const client = new sdk.Client()

  const functions = new sdk.Functions(client)

  client
    .setEndpoint(req.variables["APPWRITE_FUNCTION_ENDPOINT"])
    .setProject(req.variables["APPWRITE_FUNCTION_PROJECT_ID"])
    .setKey(req.variables["APPWRITE_FUNCTION_API_KEY"])
    .setSelfSigned(true)

  auth = {
    signup: req.variables["SIGNUP_ID"],
    login: req.variables["LOGIN_ID"],
    verify: req.variables["VERIFY_ID"],
  }

  const payload = JSON.parse(req.payload)

  let result = await functions.createExecution(
    auth[payload.flow],
    JSON.stringify(payload.data)
  )

  res.json({ ...JSON.parse(result.response) })
}
