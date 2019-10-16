var SECP256K1Client = require("jsontokens").SECP256K1Client;
var TokenSigner = require("jsontokens").TokenSigner;
var fs = require("fs");
var blockstack = require("blockstack");


function sanitizePrivKey(privKey) {
    if (privKey.length === 66 && privKey.slice(64) === "01") {
        privKey = privKey.slice(0, 64);
    }
    return privKey;
}

function generateTokenFileForContent(privateKey, content) {
    const publicKey = SECP256K1Client.derivePublicKey(privateKey);
    const tokenSigner = new TokenSigner("ES256K", privateKey);
    const payload = {
        claim: content,
        issuer: { publicKey },
        subject: { publicKey },
    };
    const token = tokenSigner.sign(payload);
    return [blockstack.wrapProfileToken(token)];
}

async function uploadContentToGaiaHub(hubURL, filename, privKey, filepath, type="application/json") {
    const sanitizedPrivKey = sanitizePrivKey(privKey);
    const hubConfig = await blockstack.connectToGaiaHub(hubURL, sanitizedPrivKey);
    let content = fs.readFileSync(filepath).toString();
    content = JSON.parse(content);
    const tokenFile = generateTokenFileForContent(sanitizedPrivKey, content);
    const contentToUpload = JSON.stringify(tokenFile);
    try {
        let finalURL = await blockstack.uploadToGaiaHub(filename, contentToUpload, hubConfig, type);
        console.log(`finalUrl is ${finalURL}`);
    } catch (error) {
        console.log("Error occured while upload:- ", error);
    }
    return true;
}

uploadContentToGaiaHub("https://hub.cruxpay.com", "cruxdev_client-config.json", "private_key_goes_here", "../resources/zel_client_config.json")
