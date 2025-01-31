// npm install jwt-decode
import { jwtDecode } from "jwt-decode";

function decodeToken(token) {
  let decoded = jwtDecode(token);

  decoded = {
    ...decoded,
    ...decoded.properties, // Merge properties into the main object
  };

  return decoded;
}


const token = "";
const decoded = decodeToken(token);
console.log(decoded);
