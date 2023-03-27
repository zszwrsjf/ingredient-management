/// decode the payload of the given JWT and return an object
export const decode = (token: string) =>
  JSON.parse(decodeURIComponent(atob(token.split('.')[1])));
