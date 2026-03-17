export const find = (arr) => (key) => (val) =>
  arr.find((x) => (key !== null ? x[key] === val : x === val));

export const map = (arr) => (fn) => arr.map(fn);

export const reduce = (arr) => (fn, init) => arr.reduce(fn, init || {});

export const filter = (arr) => (fn) => (thisArgs = null) =>
  arr.filter(fn, thisArgs || undefined);

export const every = (arr) => (fn) => (thisArgs) =>
  arr.every(fn, thisArgs || undefined);

export const some = (arr) => (fn) => (thisArgs) => arr.some(fn, thisArgs || {});

export const findIdx = (arr) => (fn) => arr.findIndex(fn);

export const flat = (arr) => arr.flat();

export const compose = (...funcs) => (...args) =>
  funcs.reduce((g, f) => f(g(...args)));

export const composeFunctions = (...funcs) => (...fns) => (arr, init) =>
  funcs.reduce(
    (g, f, idx) =>
      (g = f(g)(
        typeof fns[idx] === "function" &&
          fns[idx](f.name === "reduce" && init && init)
      )),
    arr
  );
