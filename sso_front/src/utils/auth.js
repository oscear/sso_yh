const USER_KEY = "user"
const TOKEN_KEY = "token"

class Auth {
  constructor() {
    this.token = null
    this.user = null
    this.token = sessionStorage.getItem(TOKEN_KEY)
    const userJson = sessionStorage.getItem(USER_KEY)
    if (userJson && userJson != 'undefined') {
      this.user = JSON.parse(userJson)
    }
  }

  static getInstance() {
    if (!this._instance) {
      this._instance = new Auth()
    }
    return this._instance
  }

  setUserToken(user, token) {
    this.user = user
    this.token = token
    sessionStorage.setItem(USER_KEY, JSON.stringify(user))
    sessionStorage.setItem(TOKEN_KEY, token)
  }

  setUser(user) {
    this.user = user
    sessionStorage.setItem(USER_KEY, JSON.stringify(user))
  }

  clearUserToken() {
    this.user = null;
    this.token = null;
    sessionStorage.removeItem(USER_KEY)
    sessionStorage.removeItem(TOKEN_KEY)
  }

  get is_authed() {
    if (this.user && this.token) {
      return true
    } else {
      return false
    }
  }
}


export default Auth.getInstance()