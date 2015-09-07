try { return (function (selector) {
  var el = document.querySelector(selector);
  var $injector = angular.element(el).injector();
  var $http = $injector.get('$http');
  return $http.pendingRequests;
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }