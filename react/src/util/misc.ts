export const floor = (n: number | undefined) => {
  if (n === undefined) {
    return 0;
  } else {
    return Math.floor(n);
  }
};

export const iso_to_string = (ds: string) => {
  const d = new Date(ds);
  return `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`;
};

export const trim_to_length = (ss: string, n: number) => {
  let res = ss;
  if (ss.length > n) {
    res = res.substring(0, n - 3).concat('...');
  }
  return res;
};

export const round = (value: number, precision: number) => {
  const multiplier = Math.pow(10, precision || 0);
  return Math.round(value * multiplier) / multiplier;
};

// source: https://emailregex.com/
export const emailRegEx =
  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
