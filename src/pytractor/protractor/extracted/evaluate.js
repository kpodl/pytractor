try { return (function (element, expression) {
  return angular.element(element).scope().$eval(expression);
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }