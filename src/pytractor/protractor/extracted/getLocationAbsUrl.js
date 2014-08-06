try { return (function (selector) {
  var el = document.querySelector(selector);
  return angular.element(el).injector().get('$location').absUrl();
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }